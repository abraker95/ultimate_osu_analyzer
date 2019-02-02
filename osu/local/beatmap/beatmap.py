from .beatmap_utility import BeatmapUtil
from .beatmapIO import BeatmapIO


class Beatmap(BeatmapIO):

    def __init__(self, filepath):
        super().__init__(filepath)

    
    def set_rate_mult(self, rate):
        pass


    def set_rate_bpm(self, rate):
        pass


    def get_rate_mult(self):
        pass


    def get_rate_bpm(self):
        pass


    def rotate_beatmap(self, radians):
        pass


    def flip_beatmap(self, axis_radians):
        pass


    def set_cs_val(self, cs):
        self.cs = cs


    def set_cs_px(self, px):
        self.cs = BeatmapUtil.px_to_cs(px)


    def get_cs_val(self):
        return self.cs


    def get_cs_px(self):
        return BeatmapUtil.cs_to_px(self.cs)


    def set_ar_val(self, ar):
        self.ar = ar


    def set_ar_ms(self, ms):
        self.ar = BeatmapUtil.ms_to_ar(ms)


    def get_ar_val(self):
        return self.ar


    def get_ar_ms(self):
        return BeatmapUtil.ar_to_ms(self.ar)


    def set_od_val(self, od):
        self.od = od


    def get_od_val(self):
        return self.od


    def apply_mods(self, mods):
        # TODO: return modified beatmap
        pass