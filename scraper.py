import requests
from bs4 import BeautifulSoup
from manager import Manager


class Scraper:
    
    @staticmethod
    def get_response():
        response = requests.get("https://subsplease.org/rss/?r=1080")
        soup = BeautifulSoup(response.text, "lxml")
        return soup

    def get_new_episodes(self):
        soup = self.get_response()
        manager = Manager()
        manager.load_shows_watching()
        manager.load_episodes_downloaded()
        newly_added = []
        for episode in soup.find_all("item"):
            if (
                episode.category.text in manager.shows_watching
                and episode.title.text not in manager.episodes_downloaded
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
                newly_added.append(episode_dict)
        return newly_added

    def get_all_shows(self, query: str):
        soup = self.get_response()
        all_shows = [
            category.text
            for category in soup.find_all("category")
            if query.lower() in category.text.lower()
        ]
        all_shows = list(dict.fromkeys(all_shows))
        return all_shows
