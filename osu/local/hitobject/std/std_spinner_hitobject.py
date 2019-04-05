from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.hitobject import Hitobject
from osu.local.beatmap.beatmap_utility import BeatmapUtil
from misc.math_utils import value_to_percent


"""
Visualizes the osu!std spinner

Input: 
    beatmap_data - osu!std slider data read from the beatmap file; determines pos, etc
    time - The time value of the playfield; determine's hitcircle's opacity, follow point position, etc

Output: 
    Visual display of an osu!std hitcircle
"""
class StdSpinnerHitobject(Hitobject):

    def __init__(self, data):
        Hitobject.__init__(self, data)

        self.__process_spinner_data(data)
        self.radius = 512

    
    def get_end_time(self):
        return self.end_time


    def time_changed(self, time):
        self.radius = BeatmapUtil.PLAYFIELD_HEIGHT*(1 - value_to_percent(self.time, self.end_time, time))


    def raw_data(self):
        return [ [ self.time, (self.pos.x, self.pos.y) ], [ self.end_time, (self.pos.x, self.pos.y) ] ]


    def render_hitobject_outline(self, painter, ratio_x, ratio_y):
        painter.setPen(QPen(QColor(0, 255, 255, 255), 5))

        pos_x = (self.pos.x - self.radius/2)*ratio_x
        pos_y = (self.pos.y - self.radius/2)*ratio_y
        painter.drawEllipse(pos_x, pos_y, self.radius*self.ratio_x, self.radius*ratio_y)

        center_radius = 3
        pos_x = (self.pos.x - center_radius/2)*ratio_x
        pos_y = (self.pos.y - center_radius/2)*ratio_y
        painter.drawEllipse(pos_x, pos_y, center_radius*ratio_x, center_radius*ratio_y)


    def resizeEvent(self, event):
        print('owh')


    def set_opacity(self, opacity):
        pass


    def boundingRect(self):
        return QRectF(0, 0, self.radius, self.radius)


    def __process_spinner_data(self, beatmap_data):
        self.end_time = int(beatmap_data[5])