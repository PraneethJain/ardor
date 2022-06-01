from manager import Manager
import sys

if __name__ == '__main__':
    manager = Manager()
    for arg in sys.argv:
        if arg=='dl':
            manager.update()
        if arg=='play':
            manager.play('test')