from bs4 import BeautifulSoup
from qbittorrent import Client
from rich.console import Console
from rich.table import Table
import requests
import os
import json

console = Console()


class Manager:
    def __init__(self):

        self.url = "https://subsplease.org/rss/?r=1080"

        with open("downloaded_episodes.txt") as f:
            self.episodes_downloaded = set(f.read().splitlines())
        with open("shows_watching.txt") as f:
            self.shows_watching = set(f.read().splitlines())
        with open("unwatched_episodes.json", "r") as f:
            self.episodes_unwatched = json.load(f)

    def get_response(self):
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, "lxml")

    def parse_response(self):
        self.newly_added = []
        for episode in self.soup.find_all("item"):
            if (
                episode.category.text in self.shows_watching
                and episode.title.text not in self.episodes_downloaded
            ):
                episode_dict = {
                    "title": episode.title.text,
                    "show": episode.category.text[:-7],
                    "link": episode.link.next_element,
                    "date": episode.pubdate.text[:-6],
                    "size": episode.find("subsplease:size").text,
                    "ep": episode.title.text[
                        episode.title.text.rfind("-")
                        + 2 : episode.title.text.find("(")
                        - 1
                    ],
                }
                console.print(episode_dict)
                self.newly_added.append(episode_dict)

    def update_downloaded(self):
        with open("downloaded_episodes.txt", "a") as f:
            for episode in self.newly_added:
                f.write(f"{episode['title']}\n")
                
    def update_unwatched(self):
        self.episodes_unwatched.extend(self.newly_added)
        with open("unwatched_episodes.json", "w") as f:
            json.dump(self.episodes_unwatched, f)

    def start_torrent(self, episode):
        client = Client("http://127.0.0.1:8080/")
        client.login("admin", "adminadmin")
        client.download_from_link(
            episode["link"], savepath=f"D:\Anime\{episode['show']}"
        )

    def download_all(self):
        for episode in self.newly_added:
            self.start_torrent(episode)

    def print_newly_added(self):
        if self.newly_added:
            table = Table(title="Episodes Added")
            table.add_column("S.No", justify="center")
            table.add_column("Released", justify="center", style="#c200fb")
            table.add_column("Show", justify="center", style="#ec0868")
            table.add_column("Ep", justify="center", style="#fc2f00")
            table.add_column("Quality", justify="center", style="#ec7d10")
            table.add_column("Size", justify="center", style="#ffbc0a")
            for i, episode in enumerate(self.newly_added, start=1):
                table.add_row(
                    str(i),
                    episode["date"],
                    episode["show"],
                    episode["ep"],
                    episode["title"][
                        episode["title"].find("(") + 1 : episode["title"].rfind(")")
                    ],
                    episode["size"],
                )
            console.print(table)
        else:
            console.print(f"No new episodes!")

    def update(self):
        self.get_response()
        self.parse_response()
        self.update_downloaded()
        self.update_unwatched()
        self.download_all()
        self.print_newly_added()

    def play(self, episode_path):
        episode_path = (
            "D:\Anime\Ping Pong The Animation\Episode 11 - Blood Tastes Like Iron.mkv"
        )
        os.system(f'mpv "{episode_path}"')

    def test(self):
        console.print(self.episodes_downloaded)
        console.print(self.shows_watching)
        console.print(self.newly_added)
        console.print(self.soup.prettify())
