from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.mania.mania import Mania, ManiaSettings

from misc.frozen_cls import FrozenCls



@FrozenCls
class ManiaSingleNoteHitobject(QGraphicsItem, Hitobject):

    def __init__(self):
        QGraphicsItem.__init__(self)
        Hitobject.__init__(self)


    def render_hitobject(self, painter, spatial_data, time):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(255, 0, 0, self.opacity*255))

        draw_data = self.get_draw_data(*spatial_data, time)
        painter.fillRect(QRectF(*draw_data), QBrush(QColor(255, 0, 0, self.opacity*255)))


    def get_draw_data(self, ratio_x, ratio_y, ratio_t, x_offset, y_offset, current_time):
        column = Mania.get_column(self.pos.x, self.difficulty.cs)

        scaled_note_width  = ManiaSettings.note_width*ratio_x
        scaled_note_height = ManiaSettings.note_height*ratio_y

        pos_x = x_offset + column*(ManiaSettings.note_width + ManiaSettings.note_seperation)*ratio_x
        pos_y = y_offset + (current_time - self.time)*ratio_t - scaled_note_height

        return pos_x, pos_y, scaled_note_width, scaled_note_height


    def paint(self, painter, option, widget):
        # TODO
        pass


    def resizeEvent(self, event):
        print('owh')


    def boundingRect(self):
        return QRectF(0, 0, self.radius, self.radius)