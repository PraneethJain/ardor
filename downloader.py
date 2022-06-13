from qbittorrent import Client
from manager import Manager


class Downloader:
    def __init__(
        self,
        base_directory: str = "D:\Anime",
        username: str = "admin",
        password: str = "adminadmin",
    ):
        self.base_directory = base_directory
        self.username = username
        self.password = password
        self.manager = Manager()
        self.manager.load_episodes_downloaded()
        self.manager.load_unwatched_episodes()
        
    def set_username(self, username: str):
        self.username = username
        
    def set_password(self, password: str):
        self.password = password
        
    def set_base_directory(self, base_directory: str):
        self.base_directory = base_directory

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
