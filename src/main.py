from manager import Manager
import sys

if __name__ == '__main__':
    manager = Manager()
    for i,arg in enumerate(sys.argv):
        if arg=='download' or arg=='dl':
            manager.update()
            break
        if arg=='play' or arg=='watch':
            manager.play('test')
            break
        if arg=='watchlist' or arg=='wl':
            manager.watchlist()
            break
        if arg=='complete' or arg=='cl':
            manager.complete(int(sys.argv[i+1])-1)
            break
        if arg=='test':
            manager.test()