from PyQt5.QtCore import QObject, pyqtSignal
from .beatmap_utility import BeatmapUtil
from .beatmapIO import BeatmapIO
from misc.callback import callback



'''
Description: Provides a manupilation interface for beatmaps

Input: 
    load_beatmap - load the beatmap specified

Output:
    hitobjects - list of hitobjects present in the map
    timingpoints - list of timing points present in the map
'''
class Beatmap(QObject, BeatmapIO):

    cs_changed        = pyqtSignal(float)
    ar_changed        = pyqtSignal()
    od_changed        = pyqtSignal()
    timings_changed   = pyqtSignal()
    positions_changed = pyqtSignal()


    def __init__(self, filepath):
        QObject.__init__(self)
        BeatmapIO.__init__(self, filepath)

    
    def set_rate_mult(self, rate):
        # TODO
        self.timings_changed.emit()


    def set_rate_bpm(self, rate):
        # TODO
        self.timings_changed.emit()


    def get_rate_mult(self):
        pass


    def get_rate_bpm(self):
        pass


    def rotate_beatmap(self, radians):
        # TODO
        self.positions_changed.emit()


    def flip_beatmap(self, axis_radians):
        # TODO
        self.positions_changed.emit()


    @callback
    def set_cs_val(self, cs):
        self.cs = cs
        self.set_cs_val.emit(BeatmapUtil.cs_to_px(cs))

    
    def set_cs_px(self, px):
        self.cs = BeatmapUtil.px_to_cs(px)
        self.cs_changed.emit(px)


    def get_cs_val(self):
        return self.cs


    def get_cs_px(self):
        return BeatmapUtil.cs_to_px(self.cs)


    def set_ar_val(self, ar):
        self.ar = ar
        self.ar_changed.emit()


    def set_ar_ms(self, ms):
        self.ar = BeatmapUtil.ms_to_ar(ms)
        self.ar_changed.emit()


    def get_ar_val(self):
        return self.ar


    def get_ar_ms(self):
        return BeatmapUtil.ar_to_ms(self.ar)


    def set_od_val(self, od):
        self.od = od
        self.od_changed.emit()


    def get_od_val(self):
        return self.od


    def apply_mods(self, mods):
        # TODO: return modified beatmap
        pass