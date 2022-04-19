from time import sleep
from qbittorrent import Client
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service


class Instance:
    def __init__(self):
        self.edge_options = Options()
        self.edge_options.add_argument("headless")
        self.edge_options.add_argument("disable-gpu")
        self.service = Service("msedgedriver.exe")
        self.driver = WebDriver(service=self.service, options=self.edge_options)
        self.initialize()
        self.datas = self.get_all_pages()

    def initialize(self):
        with open("links.txt") as f:
            links = f.readlines()
        self.links = [ele.strip() for ele in links]
        self.names = [link[29:-2].replace("-", " ").capitalize() for link in links]

    def get_all_pages(self):
        datas = {}
        for name, link in zip(self.names, self.links):
            datas[name] = self.generate_page_data(link)
        return datas

    def generate_page_data(self, link):
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

    @staticmethod
    def start_torrent(magnet: str, name: str) -> None:
        qb = Client("http://127.0.0.1:8080/")
        qb.login("admin", "adminadmin")
        qb.download_from_link(magnet, savepath=f"D:\Anime\{name}")

    def quit(self):
        self.driver.quit()

    def download_all(self):
        for name, values in self.datas.items():
            for episode in values:
                self.start_torrent(episode["magnet"], name)


if __name__ == "__main__":
    I = Instance()
    I.download_all()
    I.quit()
