from rich.console import Console
from rich.table import Table

import os
import sys
import json

console = Console()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Manager:
    def load_episodes_downloaded(self):
        with open(resource_path("data/downloaded_episodes.txt")) as f:
            self.episodes_downloaded = set(f.read().splitlines())

    def load_shows_watching(self):
        with open(resource_path("data/shows_watching.json"), "r") as f:
            self.shows_watching = json.load(f)

    def load_unwatched_episodes(self):
        with open(resource_path("data/unwatched_episodes.json"), "r") as f:
            self.episodes_unwatched = json.load(f)

    def update_downloaded(self, episode: dict = {}):
        with open(resource_path("data/downloaded_episodes.txt"), "a") as f:
            f.write(f"{episode['title']}\n")

    def update_unwatched(self, episode: dict = {}):
        if episode:
            self.episodes_unwatched.append(episode)
        with open(resource_path("data/unwatched_episodes.json"), "w") as f:
            json.dump(self.episodes_unwatched, f)

    def create_table(self, L, title):
        table = Table(title=title)
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

    def watchlist(self):
        if self.episodes_unwatched:
            return self.create_table(
                self.episodes_unwatched, "[bold red]Watchlist[/bold red]"
            )
        else:
            return "[yellow bold]No unwatched episodes[/yellow bold]"

    def complete(self, indices):
        output_text = ""
        for i in sorted(indices, reverse=True):
            episode = self.episodes_unwatched[i]
            del self.episodes_unwatched[i]
            self.update_unwatched()
            yield f"[green bold]Completed {episode['show']} {episode['ep']}[/green bold]"

    def add_show(self, show: str):
        self.load_shows_watching()
        if show in self.shows_watching:
            return f"[red bold]Already added[/red bold]"
        self.shows_watching.append(show)
        with open(resource_path("data/shows_watching.json"), "w") as f:
            json.dump(self.shows_watching, f)
            return f"[green bold]Added {show}[/green bold]"

    def remove_show(self, indices):
        for i in sorted(indices, reverse=True):
            removed_show = self.shows_watching[i]
            yield f"[magenta]Removed [bold]{removed_show}[/bold][/magenta]"
            del self.shows_watching[i]
        with open(resource_path("data/shows_watching.json"), "w") as f:
            json.dump(self.shows_watching, f)

    def watching_shows(self):
        table = Table(title="Shows Watching")
        table.add_column("S.No", justify="center", style="#ff0f7b")
        table.add_column("Show", justify="center", style="#f89b29")
        if shows_watching := self.shows_watching:
            for i, show in enumerate(shows_watching, start=1):
                table.add_row(str(i), show)
            return table
        else:
            return "[bold red]You haven't added any shows![/bold red]"
