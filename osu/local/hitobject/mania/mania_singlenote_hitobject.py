from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.mania.mania import Mania

from misc.frozen_cls import FrozenCls



@FrozenCls
class ManiaSingleNoteHitobject(QGraphicsItem, Hitobject):

    def __init__(self):
        QGraphicsItem.__init__(self)
        Hitobject.__init__(self)


    def render_hitobject(self, painter, draw_data, time):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(255, 0, 0, self.opacity*255))

        ratio_x, ratio_y, ratio_t, x_offset, y_offset, note_width, note_height, note_seperation = draw_data
        column = Mania.get_column(self.pos.x, self.difficulty.cs)

        scaled_note_width  = note_width*ratio_x
        scaled_note_height = note_height*ratio_y

        pos_x = x_offset + column*(note_width + note_seperation)*ratio_x
        pos_y = y_offset + (time - self.time)*ratio_t - scaled_note_height

        painter.fillRect(QRectF(pos_x, pos_y, scaled_note_width, scaled_note_height), QBrush(QColor(255, 0, 0, self.opacity*255)))


    def paint(self, painter, option, widget):
        # TODO
        pass


    def resizeEvent(self, event):
        print('owh')


    def boundingRect(self):
        return QRectF(0, 0, self.radius, self.radius)