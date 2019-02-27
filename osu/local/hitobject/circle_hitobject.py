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
class CircleHitobject(QGraphicsItem, Hitobject):

    def __init__(self, data):
        QGraphicsItem.__init__(self)
        Hitobject.__init__(self, data)


    def time_changed(self, time):
        pass


    def paint(self, painter, option, widget):
        painter.setPen(QColor(255, 0, 0, self.opacity*255))

        pos_x = (self.pos.x - self.radius)*self.ratio_x
        pos_y = (self.pos.y - self.radius)*self.ratio_y
        painter.drawEllipse(pos_x, pos_y, 2*self.radius*self.ratio_x, 2*self.radius*self.ratio_y)


    def resizeEvent(self, event):
        print('owh')


    def boundingRect(self):
        return QRectF(0, 0, self.radius, self.radius)