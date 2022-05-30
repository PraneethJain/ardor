from bs4 import BeautifulSoup
from qbittorrent import Client
from rich import print
import requests


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
                self.magnets.add((episode.link.next_element, episode.category.text[:-7]))
                self.newly_added.add(episode.title.text)

    def update_downloaded(self):
        with open("downloaded_episodes.txt", "a") as f:
            for title in self.newly_added:
                f.write(f"{title}\n")
                
    def start_torrent(self, magnet, show):
        client = Client("http://127.0.0.1:8080/")
        client.login("admin", "adminadmin")
        client.download_from_link(magnet, savepath=f"D:\Anime\{show}")

    def download_all(self):
        for magnet,show in self.magnets:
            self.start_torrent(magnet, show)
            
    def print_newly_added(self):
        if self.newly_added:
            for title in self.newly_added:
                print(f"Added: {title}")
        else:
            print(f"No new episodes!")
    
    def do(self):
        self.get_response()
        self.parse_response()
        self.update_downloaded()
        self.download_all()
        self.print_newly_added()
        
    def test(self):
        print(self.episodes_downloaded)
        print(self.shows_watching)
        print(self.newly_added)
        print(self.soup.prettify())
    

if __name__ == "__main__":

    downloader = Downloader()
    downloader.do()
