from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.std.std import Std

from misc.frozen_cls import FrozenCls
from misc.math_utils import value_to_percent



"""
Visualizes the osu!std spinner

Input: 
    beatmap_data - osu!std slider data read from the beatmap file; determines pos, etc
    time - The time value of the playfield; determine's hitcircle's opacity, follow point position, etc

Output: 
    Visual display of an osu!std hitcircle
"""
@FrozenCls
class StdSpinnerHitobject(Hitobject):

    def __init__(self, beatmap=None):
        self.beatmap  = beatmap
        self.end_time = None

        Hitobject.__init__(self)

    
    def get_end_time(self):
        return self.end_time


    def raw_data(self):
        return [ [ self.time, (self.pos.x, self.pos.y) ], [ self.end_time, (self.pos.x, self.pos.y) ] ]


    def render_hitobject_outline(self, painter, ratio_x, ratio_y, time):
        painter.setPen(QPen(QColor(0, 255, 255, 255), 5))

        outer_radius = Std.PLAYFIELD_HEIGHT*(1 - value_to_percent(self.time, self.end_time, time))
        pos_x = (self.pos.x - outer_radius/2)*ratio_x
        pos_y = (self.pos.y - outer_radius/2)*ratio_y
        painter.drawEllipse(pos_x, pos_y, outer_radius*ratio_x, outer_radius*ratio_y)

        center_radius = 3
        pos_x = (self.pos.x - center_radius/2)*ratio_x
        pos_y = (self.pos.y - center_radius/2)*ratio_y
        painter.drawEllipse(pos_x, pos_y, center_radius*ratio_x, center_radius*ratio_y)


    def resizeEvent(self, event):
        print('owh')


    def set_opacity(self, opacity):
        pass


    def boundingRect(self):
        radius = BeatmapUtil.cs_to_px(self.difficulty.cs)
        return QRectF(0, 0, radius, radius)

