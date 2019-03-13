from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.hitobject import Hitobject
from osu.local.beatmap.beatmap_utility import BeatmapUtil


"""
Visualizes the osu!std hitcircle

Input: 
    beatmap_data - osu!std slider data read from the beatmap file; determines pos, etc
    time - The time value of the playfield; determine's hitcircle's opacity, follow point position, etc

Output: 
    Visual display of an osu!std hitcircle
"""
class StdSingleNoteHitobject(Hitobject):

    def __init__(self, data):
        Hitobject.__init__(self, data)


    def render_hitobject_outline(self, painter, ratio_x, ratio_y):
        painter.setPen(QColor(255, 0, 0, self.opacity*255))

        pos_x = (self.pos.x - self.radius)*ratio_x
        pos_y = (self.pos.y - self.radius)*ratio_y
        painter.drawEllipse(pos_x, pos_y, 2*self.radius*ratio_x, 2*self.radius*ratio_y)


    def render_hitobject_aimpoints(self, painter, ratio_x, ratio_y):
        painter.setPen(QColor(255, 0, 255, self.opacity*255))
        aimpoint_radius = 6

        pos_x = (self.pos.x - 0.5*aimpoint_radius)*ratio_x
        pos_y = (self.pos.y - 0.5*aimpoint_radius)*ratio_y
        painter.drawEllipse(pos_x, pos_y, aimpoint_radius, aimpoint_radius)



    def resizeEvent(self, event):
        print('owh')


    def boundingRect(self):
        return QRectF(0, 0, self.radius, self.radius)