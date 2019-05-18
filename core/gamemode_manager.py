from generic.switcher import Switcher
from core.metric_manager import MetricManager
from osu.local.beatmap.beatmap import Beatmap


class GamemodeManager(Switcher):

    def __init__(self):
        Switcher.__init__(self)

        self.add(Beatmap.GAMEMODE_OSU,   MetricManager())
        self.add(Beatmap.GAMEMODE_MANIA, MetricManager())
        self.add(Beatmap.GAMEMODE_TAIKO, MetricManager())
        self.add(Beatmap.GAMEMODE_CATCH, MetricManager())


    def get_metric_lib(self, gamemode):
        return self.data[gamemode]


    def set_gamemode(self, gamemode):
        self.switch(gamemode)


gamemode_manager = GamemodeManager()