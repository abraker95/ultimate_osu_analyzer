from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.std.std import Std

from misc.frozen_cls import FrozenCls



"""
Visualizes the osu!std hitcircle

Input: 
    beatmap_data - osu!std slider data read from the beatmap file; determines pos, etc
    time - The time value of the playfield; determine's hitcircle's opacity, follow point position, etc

Output: 
    Visual display of an osu!std hitcircle
"""
@FrozenCls
class StdSingleNoteHitobject(Hitobject):

    def __init__(self):
        Hitobject.__init__(self)


    def render_hitobject_outline(self, painter, ratio_x, ratio_y, time):
        painter.setPen(QColor(0, 0, 255, self.opacity*255))
        painter.setBrush(QColor(0, 0, 255, self.opacity*25))

        radius = Std.cs_to_px(self.difficulty.cs)
        pos_x  = (self.pos.x - radius)*ratio_x
        pos_y  = (self.pos.y - radius)*ratio_y
        painter.drawEllipse(pos_x, pos_y, 2*radius*ratio_x, 2*radius*ratio_y)


    def render_hitobject_aimpoints(self, painter, ratio_x, ratio_y):
        painter.setPen(QColor(255, 0, 255, self.opacity*255))
        aimpoint_radius = 3

        pos_x = (self.pos.x - aimpoint_radius)*ratio_x
        pos_y = (self.pos.y - aimpoint_radius)*ratio_y
        painter.drawEllipse(pos_x, pos_y, 2*aimpoint_radius*ratio_x, 2*aimpoint_radius*ratio_y)


    def time_to_pos(self, time):
        return self.pos
        

    def get_aimpoint_times(self):
        return [ self.time ]


    def raw_data(self):
        return [ [ self.time, (self.pos.x, self.pos.y) ] ]


    def resizeEvent(self, event):
        print('owh')


    def boundingRect(self):
        radius = BeatmapUtil.cs_to_px(self.difficulty.cs)
        return QRectF(0, 0, radius, radius)