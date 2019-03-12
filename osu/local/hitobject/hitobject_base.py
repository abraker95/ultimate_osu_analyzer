from misc.pos import Pos
from misc.callback import callback



"""
Abstract object that holds common hitoobject data
obtained during reading hitobject data

Input: 
    beatmap_data - hitobject data read from the beatmap file
"""
class HitobjectBase():

    CIRCLE  = 1 << 0
    SLIDER  = 1 << 1
    NCOMBO  = 1 << 2
    SPINNER = 1 << 3
    # ???
    MANIALONG = 1 << 7

    def __init__(self, beatmap_data=None):

        if beatmap_data is None:
            self.hitobject_type = None
            self.new_combo      = None
            self.time           = None
            self.pos            = None

        if beatmap_data:
            self.__process_hitobject_data(beatmap_data)


    def get_copy(self):
        pass


    def get_end_time(self):
        return self.time


    def is_hitobject_type(self, hitobject_type):
        return self.hitobject_type & hitobject_type > 0


    @callback
    def set_timing(self, ms):
        self.time = ms
        self.set_timing.emit(ms)


    @callback
    def set_postition(self, pos):
        self.pos = pos
        self.set_postition.emit(pos)


    def __process_hitobject_data(self, data):
        self.pos            = Pos(int(data[0]), int(data[1]))
        self.time           = int(data[2])
        self.hitobject_type = int(data[3])
        self.new_combo      = self.is_hitobject_type(HitobjectBase.NCOMBO)