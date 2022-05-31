from rich import print
import os


class Player:
    
    def __init__(self) -> None:
        os.environ["PATH"] += f"{os.getcwd()}\\libmpv"
        import mpv
