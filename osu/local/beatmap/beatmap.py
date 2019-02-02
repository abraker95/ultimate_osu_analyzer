from beatmapIO import BeatmapIO


class Beatmap(BeatmapIO):

    def __init__(self):
        pass

    
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
        pass


    def get_cs_val(self):
        return self.cs


    def get_cs_px(self):
        pass


    def set_ar_val(self, ar):
        self.ar = ar


    def set_ar_ms(self, ms):
        pass


    def get_ar_val(self):
        return self.ar


    def get_ar_ms(self):
        pass


    def set_od_val(self, od):
        self.od = od


    def get_od_val(self):
        return self.od


    def apply_mods(self, mods):
        # TODO: return modified beatmap
        pass