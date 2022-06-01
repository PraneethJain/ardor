from manager import Manager
import sys

if __name__ == '__main__':
    manager = Manager()
    for arg in sys.argv:
        if arg=='download' or arg=='dl':
            manager.update()
        if arg=='play' or arg=='watch':
            manager.play('test')
        if arg=='watchlist' or arg=='wl':
            manager.watchlist()
        if arg=='test':
            manager.test()