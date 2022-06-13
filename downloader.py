from email.mime import base
from qbittorrent import Client
from manager import Manager, resource_path
import json


class Downloader:
    def __init__(self):
        self.cred = self.get_cred()
        self.base_directory = self.cred["base_directory"]
        self.username = self.cred["username"]
        self.password = self.cred["password"]
        self.manager = Manager()
        self.manager.load_episodes_downloaded()
        self.manager.load_unwatched_episodes()

    def get_cred(self):
        with open(resource_path("data/cred.json"), "r") as f:
            return json.load(f)

    def set_username(self, username: str):
        cred = self.get_cred()
        cred["username"] = username
        with open(resource_path("data/cred.json"), "w") as f:
            json.dump(cred, f)

    def set_password(self, password: str):
        cred = self.get_cred()
        cred["password"] = password
        with open(resource_path("data/cred.json"), "w") as f:
            json.dump(cred, f)

    def set_base_directory(self, base_directory: str):
        cred = self.get_cred()
        cred["base_directory"] = base_directory
        with open(resource_path("data/cred.json"), "w") as f:
            json.dump(cred, f)

    def start_torrent(self, episode):
        client = Client("http://127.0.0.1:8080/")
        client.login(self.username, self.password)
        client.download_from_link(
            episode["link"],
            savepath=f"{self.base_directory}\{episode['show']}",
            category="anime",
        )
        self.manager.update_unwatched(episode)
        self.manager.update_downloaded(episode)
        return f"[bold blue]Started downloading {episode['show']} {episode['ep']}[/bold blue]"
