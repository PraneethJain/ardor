from manager import Manager
from player import Player
import sys

if __name__ == '__main__':
    manager = Manager()
    for arg in sys.argv:
        if arg=='dl':
            manager.update()
        if arg=='play':
            pass