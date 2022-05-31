from downloader import Downloader
from player import Player
import sys

if __name__ == '__main__':
    downloader = Downloader()
    for arg in sys.argv:
        if arg=='dl':
            downloader.update()
