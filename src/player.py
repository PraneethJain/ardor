from rich import print
import os


class Player:
    def __init__(self) -> None:
        os.environ["PATH"] += f"{os.getcwd()}\\libmpv"
        import mpv

        self.player = mpv.MPV(
            log_handler=self.log,
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True,
        )
        self.player.fullscreen = True
        self.player.autofit = "50%"

    def log(self, loglevel, component, message):
        print("[{}] {}: {}".format(loglevel, component, message))

    def play(self, episode):
        self.player.play(
            r"D:\Anime\Sabikui Bisco\[SubsPlease] Sabikui Bisco - 03 (1080p) [5ACCAE69].mkv"
        )
        self.player.wait_for_playback()
