from rich import print
import os


class Player:
    def __init__(self) -> None:
        command = r'mpv "D:\Anime\Ping Pong The Animation\Episode 11 - Blood Tastes Like Iron.mkv"'
        print(command)
        os.system(command)
