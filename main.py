from manager import Manager
import sys

if __name__ == "__main__":
    manager = Manager()
    for i, arg in enumerate(sys.argv):
        if arg == "download" or arg == "dl":
            manager.update()
            break
        if arg == "play" or arg == "watch":
            manager.play(int(sys.argv[i + 1]) - 1)
            break
        if arg == "add":
            for arg in sys.argv[i + 1 :]:
                manager.add_show(int(arg) - 1)
        if arg == "remove":
            for arg in sys.argv[i + 1 :]:
                manager.remove_show(int(arg) - 1)
        if arg == "watchlist" or arg == "wl":
            manager.watchlist()
            break
        if arg == "complete" or arg == "cl":
            manager.complete(int(sys.argv[i + 1]) - 1)
            break
        if arg == "progress":
            manager.show_progress()
            break
        if arg == "series":
            if i < len(sys.argv) - 1:
                if sys.argv[i + 1] == "all":
                    manager.list_shows()
                elif sys.argv[i + 1] == "remove":
                    if i + 1 < len(sys.argv) - 1:
                        manager.remove_show(int(sys.argv[i + 2]) - 1)
            else:
                manager.list_watching_shows()
            break
        if arg == "test":
            manager.test()
            break