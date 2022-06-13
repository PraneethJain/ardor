from typer import Typer
from manager import Manager
from downloader import Downloader
from scraper import Scraper
from rich.console import Group
from rich.live import Live
from rich import print
from msvcrt import getch

cli = Typer()


def selection_menu(options: list[str], transient=False):
    def generate_text(index):
        renderables = []
        for i, option in enumerate(options, start=1):
            if index == i:
                renderables.append(f"[magenta bold]{option}[/magenta bold]")
            else:
                renderables.append(f"[blue]{option}[/blue]")
        return Group(*renderables)

    with Live(generate_text(1), auto_refresh=False, transient=transient) as live:
        i = 1
        selected = False
        while True:
            key = ord(getch())
            changed = False
            if key == 80:  # Down Arrow
                i += 1
                if i > len(options):
                    i = 1
                changed = True
            elif key == 72:  # Up Arrow
                i -= 1
                if i < 1:
                    i = len(options)
                changed = True
            elif key == 13:  # Enter
                selected = True
                break
            if changed:
                live.update(generate_text(i))
                live.refresh()
                changed = False
    if selected:
        return i - 1, options[i - 1]


@cli.command()
def shows():
    manager = Manager()
    manager.load_shows_watching()
    print(manager.watching_shows())


@cli.command()
def play():
    manager = Manager()
    manager.load_unwatched_episodes()
    index, _ = selection_menu(
        list(map(lambda x: f"{x['show']} {x['ep']}", manager.episodes_unwatched))
    )
    manager.play(index)


@cli.command()
def add(query: str):
    scraper = Scraper()
    _, selected_show = selection_menu(scraper.get_all_shows(query))
    manager = Manager()
    print(manager.add_show(selected_show))


@cli.command()
def remove(all: bool = False):
    manager = Manager()
    manager.load_shows_watching()
    index, _ = selection_menu(manager.shows_watching)
    print(manager.remove_show(index))


@cli.command()
def download():
    scraper = Scraper()
    newly_added = scraper.get_new_episodes()
    if newly_added:
        print("[bold green]Episodes available for download![/bold green]")
        i, selection = selection_menu(
            list(map(lambda x: f"{x['show']} {x['ep']}", newly_added))
            + ["Download all"],
            transient=True,
        )
        downloader = Downloader()
        if selection == "Download all":
            for episode in newly_added:
                print(downloader.start_torrent(episode))
        else:
            episode = newly_added[i]
            print(downloader.start_torrent(episode))
    else:
        print("[red bold]No new episodes![/red bold]")


@cli.command()
def complete(all: bool = False):
    manager = Manager()
    manager.load_unwatched_episodes()
    if manager.episodes_unwatched:
        i, selection = selection_menu(
            list(map(lambda x: f"{x['show']} {x['ep']}", manager.episodes_unwatched))
            + ["Complete all"],
            transient=True,
        )
        if selection == "Complete all":
            for _ in range(len(manager.episodes_unwatched)):
                print(manager.complete(0))
        else:
            print(manager.complete(i))
    else:
        print("[yellow bold]No unwatched episodes[/yellow bold]")


@cli.command()
def watchlist():
    manager = Manager()
    manager.load_unwatched_episodes()
    print(manager.watchlist())


@cli.command()
def username(username: str):
    downloader = Downloader()
    downloader.set_username(username)


@cli.command()
def password(password: str):
    downloader = Downloader()
    downloader.set_password(password)


@cli.command()
def directory(base_directory: str):
    downloader = Downloader()
    downloader.set_base_directory(base_directory)


if __name__ == "__main__":
    cli()
