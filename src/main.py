import requests
from rich import print
from bs4 import BeautifulSoup

with open("downloaded_episodes.txt") as f:
    downloaded_episodes = set(f.read().splitlines())
with open("shows_watching.txt") as f:
    shows_watching = set(f.read().splitlines())

r = requests.get("https://subsplease.org/rss/?r=1080")
soup = BeautifulSoup(r.text, "lxml")


magnets = set()
newly_added = set()


def update_episode(episode):
    magnets.add(episode.link.next_element)
    newly_added.add(episode.title.text)


[
    update_episode(episode)
    for episode in soup.find_all("item")
    if (episode.category.text in shows_watching)
    and (episode.title.text not in downloaded_episodes)
]

with open("downloaded_episodes.txt", "a") as f:
    for title in newly_added:
        f.write(f"{title}\n")

print(magnets)
