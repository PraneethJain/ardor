from typer import Typer
from manager import Manager
from downloader import Downloader
from scraper import Scraper
from rich.console import Group
from rich.live import Live
from rich import print
from msvcrt import getch
import os

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
            elif key == 27:  # Escape
                break
            if changed:
                live.update(generate_text(i))
                live.refresh()
                changed = False
    if selected:
        return i - 1, options[i - 1]


def selection_menu_mutiple(options: list[str], transient=False):
    def generate_text(selected_indices: list[int], current_index):
        renderables = []
        for i, option in enumerate(options):
            if i in selected_indices:
                if i == current_index:
                    renderables.append(f"[magenta bold]>(●) {option}[/magenta bold]")
                else:
                    renderables.append(f" [magenta bold](●) {option}[/magenta bold]")
            elif i == current_index:
                renderables.append(f"[cyan bold]>(○) {option}[/cyan bold]")
            else:
                renderables.append(f" [blue](○) {option}[/blue]")
        return Group(*renderables)

    selected_indices = []
    selected_options = []
    i = 0

    with Live(
        generate_text(selected_indices, i), auto_refresh=False, transient=transient
    ) as live:
        while True:
            key = ord(getch())
            changed = False
            if key == 80:  # Down Arrow
                i += 1
                if i == len(options):
                    i = 0
                changed = True
            elif key == 72:  # Up Arrow
                i -= 1
                if i == -1:
                    i = len(options) - 1
                changed = True
            elif key == 32:  # Spacebar
                if i not in selected_indices:
                    selected_indices.append(i)
                    selected_options.append(options[i])
                else:
                    selected_indices.remove(i)
                    selected_options.remove(options[i])
                changed = True
            elif key == 13:  # Enter
                return selected_indices, selected_options
            elif key == 27:  # Escape
                return
            if changed:
                live.update(generate_text(selected_indices, i))
                live.refresh()
                changed = False


@cli.command()
def shows():
    manager = Manager()
    manager.load_shows_watching()
    print(manager.watching_shows())


@cli.command()
def play():
    manager = Manager()
    manager.load_unwatched_episodes()
    if not manager.episodes_unwatched:
        print("[red bold]No episodes in watchlist[/red bold]")
    else:
        i, _ = selection_menu(
            list(map(lambda x: f"{x['show']} {x['ep']}", manager.episodes_unwatched))
        )
        downloader = Downloader()
        episode_path = f"{downloader.base_directory}\{manager.episodes_unwatched[i]['show']}\{manager.episodes_unwatched[i]['title']}"
        os.system(f'"{episode_path}"')


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
    indices, _ = selection_menu_mutiple(manager.shows_watching)
    for output in manager.remove_show(indices):
        print(output)


@cli.command()
def download():
    scraper = Scraper()
    if newly_added := scraper.get_new_episodes():
        print("[bold green]Episodes available for download![/bold green]")
        if (
            a := selection_menu_mutiple(
                list(map(lambda x: f"{x['show']} {x['ep']}", newly_added)),
                transient=True,
            )
        ) is not None:
            selection_indices, _ = a
            downloader = Downloader()
            for index in selection_indices:
                print(downloader.start_torrent(newly_added[index]))
        else:
            print("[red bold]No episode selected[red bold]")
    else:
        print("[red bold]No new episodes![/red bold]")


@cli.command()
def complete():
    manager = Manager()
    manager.load_unwatched_episodes()
    if manager.episodes_unwatched:
        selected_indices, _ = selection_menu_mutiple(
            list(map(lambda x: f"{x['show']} {x['ep']}", manager.episodes_unwatched)),
            transient=True,
        )
        j = 0
        for output in manager.complete(selected_indices):
            print(output)
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
