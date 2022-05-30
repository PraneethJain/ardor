from bs4 import BeautifulSoup
from qbittorrent import Client
from rich.console import Console
from rich.table import Table
import requests

console = Console()


class Downloader:
    def __init__(self):

        self.url = "https://subsplease.org/rss/?r=1080"

        with open("downloaded_episodes.txt") as f:
            self.episodes_downloaded = set(f.read().splitlines())
        with open("shows_watching.txt") as f:
            self.shows_watching = set(f.read().splitlines())

    def get_response(self):
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, "lxml")

    def parse_response(self):
        self.magnets = set()
        self.newly_added = set()
        for episode in self.soup.find_all("item"):
            if (
                episode.category.text in self.shows_watching
                and episode.title.text not in self.episodes_downloaded
            ):
                self.magnets.add(
                    (episode.link.next_element, episode.category.text[:-7])
                )
                self.newly_added.add(episode)

    def update_downloaded(self):
        with open("downloaded_episodes.txt", "a") as f:
            for episode in self.newly_added:
                f.write(f"{episode.title.text}\n")

    def start_torrent(self, magnet, show):
        client = Client("http://127.0.0.1:8080/")
        client.login("admin", "adminadmin")
        client.download_from_link(magnet, savepath=f"D:\Anime\{show}")

    def download_all(self):
        for magnet, show in self.magnets:
            self.start_torrent(magnet, show)

    def print_newly_added(self):
        if self.newly_added:
            table = Table(title="Episodes Added")
            table.add_column("Released", justify="center", style="#c200fb")
            table.add_column("Show", justify="center", style="#ec0868")
            table.add_column("Ep", justify="center", style="#fc2f00")
            table.add_column("Quality", justify="center", style="#ec7d10")
            table.add_column("Size", justify="center", style="#ffbc0a")
            for episode in self.newly_added:
                table.add_row(
                    episode.pubdate.text[:-6],
                    episode.category.text[:-7],
                    episode.title.text[
                        episode.title.text.rfind("-")
                        + 2 : episode.title.text.find("(")
                        - 1
                    ],
                    episode.title.text[
                        episode.title.text.find("(") + 1 : episode.title.text.rfind(")")
                    ],
                    episode.find("subsplease:size").text,
                )
            console.print(table)
        else:
            console.print(f"No new episodes!")

    def do(self):
        self.get_response()
        self.parse_response()
        self.update_downloaded()
        self.download_all()
        self.print_newly_added()

    def test(self):
        console.print(self.episodes_downloaded)
        console.print(self.shows_watching)
        console.print(self.newly_added)
        console.print(self.soup.prettify())


if __name__ == "__main__":

    downloader = Downloader()
    downloader.do()
