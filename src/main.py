import requests
from rich import print
from bs4 import BeautifulSoup

with open("downloaded_episodes.txt") as f:
    downloaded_episodes = set(f.read().splitlines())
with open("shows_watching.txt") as f:
    shows_watching = set(f.read().splitlines())

url = "https://subsplease.org/rss/?r=1080"
r = requests.get("https://subsplease.org/rss/?r=1080")
soup = BeautifulSoup(r.text, "lxml")
print(soup.rss.channel.item.link.next_element)
magnets = set()
for episode in soup.find_all("item"):
    if episode.category.text in shows_watching:
        magnets.add(episode.link.next_element)

print(magnets)
