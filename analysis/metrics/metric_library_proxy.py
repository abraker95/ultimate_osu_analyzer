from gui.objects.abstract_state_manager import AbstractStateManager
from analysis.metrics.metric_library import MetricLibrary
from osu.local.beatmap.beatmap import Beatmap


class MetricLibraryProxy(AbstractStateManager):

    def __init__(self):
        AbstractStateManager.__init__(self)

        self.add(MetricLibrary(), Beatmap.GAMEMODE_OSU)
        self.add(MetricLibrary(), Beatmap.GAMEMODE_MANIA)
        self.add(MetricLibrary(), Beatmap.GAMEMODE_TAIKO)
        self.add(MetricLibrary(), Beatmap.GAMEMODE_CATCH)

    
    def get_active_lib(self):
        return self.active_state


    def get_metric_lib(self, gamemode):
        return self.abstract_states[gamemode]


    def set_gamemode(self, gamemode):
        self.switch_to(gamemode)


MetricLibraryProxy.proxy = MetricLibraryProxy()