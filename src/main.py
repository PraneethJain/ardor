from time import sleep
from rich import print
from rich.progress import track
from qbittorrent import Client
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service


class Instance:
    def __init__(self) -> None:
        """Initialize the browser instance
        Reads the links from the links.txt file
        Finds all the 1080p magnet links on those links
        """
        self.edge_options = Options()
        self.edge_options.add_argument("headless")
        self.edge_options.add_argument("disable-gpu")
        self.edge_options.add_argument("--log-level=3")
        self.edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.service = Service("msedgedriver.exe")
        self.driver = WebDriver(service=self.service, options=self.edge_options)
        with open("links.txt") as f:
            self.links = [ele.strip() for ele in f.readlines()]
        with open("magnets_added.txt") as f:
            self.already_added = [ele.strip() for ele in f.readlines()]
        self.names = [link[29:-1].replace("-", " ").capitalize() for link in self.links]
        self.datas = self.get_all_pages()
        self.added_now = []

    def get_all_pages(self) -> dict:
        """Finds magnet links and names from all the links

        Returns:
            dict: dictionary with having keys as name of the series values containing episode numbers and their magnet links
        """
        datas = {}
        for i in track(range(len(self.names)), "[purple]Getting [italic]magnet[/italic] links[/purple]  "):
            datas[self.names[i]] = self.generate_page_data(self.links[i])
        return datas

    def generate_page_data(self, link: str) -> list:
        """Finds magnet links and episode numbers from the given link

        Args:
            link (str): url of website

        Returns:
            list: list consisting of dictionaries having keys "episode" and "magnet" which contain episode number and magnet link of that episode number respectively
        """
        data = []
        self.driver.get(link)
        sleep(1)
        for element in self.driver.find_elements(By.CLASS_NAME, "show-release-item"):

            data.append(
                {
                    "episode": element.text.split()[-1],
                    "magnet": element.find_element(
                        By.XPATH,
                        ".//a[contains(@href, '1080p')][contains(@href, 'magnet')]",
                    ).get_attribute("href"),
                }
            )
        return data

    def start_torrent(self, magnet: str, name: str) -> None:
        """Starts downloading the given magnet, directory is created using name

        Args:
            magnet (str): magnet link of the torrent
            name (str): used to create the directory to save the files to
        """
        qb = Client("http://127.0.0.1:8080/")
        qb.login("admin", "adminadmin")
        qb.download_from_link(magnet, savepath=f"D:\Anime\{name}")
        self.added_now.append(magnet)

    def download_all(self) -> None:
        """Downloads from all the magnet urls which haven't already been downloaded"""
        for name, values in track(self.datas.items(), "[purple]Initializing [italic]downloads[/italic][/purple]"):
            for episode in values:
                if episode["magnet"] not in self.already_added:
                    self.start_torrent(episode["magnet"], name)
        with open("magnets_added.txt", "a") as f:
            for m in self.added_now:
                f.write(f"{m}\n")
        if self.added_now:
            for magnet in self.added_now:
                print(f"[green]Added: [italic]{self.magnet_to_name(magnet)}[/italic][/green]")
        else:
            print(f"[green]No new episodes available![/green]")
        print("[red][bold]Completed![/bold][/red]")

    @staticmethod
    def magnet_to_name(magnet: str) -> str:
        """Converts the magnet url into readable name

        Args:
            magnet (str): the magnet url to convert

        Returns:
            str: the converted final string
        """
        return (
            magnet[
                magnet.find("SubsPlease")
                + len("SubsPlease")
                + 6 : magnet.find("0p")
                + 2
            ]
            .replace("%20", " ")
            .replace("%28", "")
            .replace("%29", "")
        )

    def quit(self) -> None:
        """Quits the browser instance"""
        self.driver.quit()


if __name__ == "__main__":
    I = Instance()
    I.download_all()
    I.quit()
