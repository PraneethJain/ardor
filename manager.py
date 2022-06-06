from bs4 import BeautifulSoup
from qbittorrent import Client
from rich.console import Console
from rich.table import Table
import requests
import os
import sys
import json

console = Console()

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Manager:
    def __init__(self):

        self.url = "https://subsplease.org/rss/?r=1080"

        with open(resource_path("data/downloaded_episodes.txt")) as f:
            self.episodes_downloaded = set(f.read().splitlines())

        with open(resource_path("data/shows_watching.json"), "r") as f:
            self.shows_watching = json.load(f)
        with open(resource_path("data/unwatched_episodes.json"), "r") as f:
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
                self.newly_added.append(episode_dict)
        self.episodes_unwatched.extend(self.newly_added)

    def update_downloaded(self):
        with open(resource_path("data/downloaded_episodes.txt"), "a") as f:
            for episode in self.newly_added:
                f.write(f"{episode['title']}\n")

    def update_unwatched(self):
        with open(resource_path("data/unwatched_episodes.json"), "w") as f:
            json.dump(self.episodes_unwatched, f)

    def start_torrent(self, episode):
        client = Client("http://127.0.0.1:8080/")
        client.login("admin", "adminadmin")
        client.download_from_link(
            episode["link"], savepath=f"D:\Anime\{episode['show']}", category="anime"
        )

    def download_all(self):
        for episode in self.newly_added:
            self.start_torrent(episode)

    def create_table(self, L):
        table = Table(title="Episodes Added")
        table.add_column("S.No", justify="center")
        table.add_column("Released", justify="center", style="#c200fb")
        table.add_column("Show", justify="center", style="#ec0868")
        table.add_column("Ep", justify="center", style="#fc2f00")
        table.add_column("Quality", justify="center", style="#ec7d10")
        table.add_column("Size", justify="center", style="#ffbc0a")
        for i, episode in enumerate(L, start=1):
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
        return table

    def print_newly_added(self):
        if self.newly_added:
            console.print(self.create_table(self.newly_added))
        else:
            console.print(f"No new episodes!")

    def show_progress(self):
        client = Client("http://127.0.0.1:8080/")
        client.login("admin", "adminadmin")
        if torrents := client.torrents(filter="downloading", category="anime"):
            table = Table(title="Episodes downloading")
            table.add_column("S.No", justify="center", style="#04e762")
            table.add_column("Torrent Title", justify="center", style="#f5b700")
            table.add_column("Download %", justify="center", style="#dc0073")
            table.add_column("ETA", justify="center", style="#008bf8")
            for i, torrent in enumerate(torrents, start=1):
                table.add_row(
                    str(i),
                    torrent["name"],
                    f"{round(torrent['progress']*100, 2)}%",
                    f"{torrent['eta']//60}m {torrent['eta']%60}s",
                )
            console.print(table)
        else:
            console.print("All downloads complete!")

    def update(self):
        self.get_response()
        self.parse_response()
        self.update_downloaded()
        self.update_unwatched()
        self.download_all()
        self.print_newly_added()

    def play(self, i):
        episode_path = f"D:\Anime\{self.episodes_unwatched[i]['show']}\{self.episodes_unwatched[i]['title']}"
        os.system(f'mpv "{episode_path}"')

    def watchlist(self):
        if self.episodes_unwatched:
            console.print(self.create_table(self.episodes_unwatched))
        else:
            console.print(f"All caught up!")

    def complete(self, i):
        console.print(
            f"Completed {self.episodes_unwatched[i]['show']} {self.episodes_unwatched[i]['ep']}"
        )
        self.episodes_unwatched.pop(i)
        self.update_unwatched()

    def get_all_shows(self):
        self.get_response()
        self.all_shows = [category.text for category in self.soup.find_all("category")]
        self.all_shows = list(dict.fromkeys(self.all_shows))

    def list_shows(self):
        self.get_all_shows()
        for i, show in enumerate(self.all_shows, start=1):
            console.print(
                f"[#dc2f02]{i}[/#dc2f02]. [#f48c06]{show}[/#f48c06]", style="red"
            )

    def add_show(self, i):
        self.get_all_shows()
        self.shows_watching.append(self.all_shows[i])
        with open(resource_path("data/shows_watching.json"), "w") as f:
            json.dump(self.shows_watching, f)
            console.print(f"Added {self.all_shows[i]}")

    def list_watching_shows(self):
        table = Table(title="Shows Watching")
        table.add_column("S.No", justify="center", style="#ff0f7b")
        table.add_column("Show", justify="center", style="#f89b29")
        if shows_watching := self.shows_watching:
            for i, show in enumerate(shows_watching, start=1):
                table.add_row(str(i), show)
            console.print(table)
        else:
            console.print("You haven't added any shows!")

    def remove_show(self, i):
        removed_show = self.shows_watching.pop(i)
        with open(resource_path("data/shows_watching.json"), "w") as f:
            json.dump(self.shows_watching, f)
            console.print(f"Removed {removed_show}")

    def test(self):
        console.print(self.episodes_downloaded)
        console.print(self.shows_watching)
        console.print(self.newly_added)
        console.print(self.soup.prettify())
