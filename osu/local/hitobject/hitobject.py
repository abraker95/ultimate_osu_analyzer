from PyQt5 import QtCore
from misc.pos import Pos

from misc.frozen_cls import FrozenCls


"""
Abstract object that holds common hitoobject data

Input: 
    beatmap_data - hitobject data read from the beatmap file
"""
@FrozenCls
class Hitobject():

    CIRCLE  = 1 << 0
    SLIDER  = 1 << 1
    NCOMBO  = 1 << 2
    SPINNER = 1 << 3
    # ???
    MANIALONG = 1 << 7

    def __init__(self):

        self.hitobject_type = None
        self.time  = None
        self.index = None
        self.pos   = None

        self.difficulty = None
        self.opacity    = 1.0


    def get_copy(self):
        pass


    def get_end_time(self):
        try:    return self.end_time
        except: return self.time

 
    def raw_data(self):
        return [ [ self.time, (self.pos.x, self.pos.y) ] ]


    def is_hitobject_type(self, hitobject_type):
        return self.hitobject_type & hitobject_type > 0


    def is_hitobject_long(self):
        return self.is_hitobject_type(Hitobject.SLIDER) or self.is_hitobject_type(Hitobject.MANIALONG)


    def time_changed(self, time):
        pass


    def set_timing(self, ms):
        self.time = ms


    def set_opacity(self, opacity):
        self.opacity = opacity


    def set_postition(self, pos):
        self.pos = pos


    def set_ratios(self, ratio_x, ratio_y):
        self.ratio_x = ratio_x
        self.ratio_y = ratio_y