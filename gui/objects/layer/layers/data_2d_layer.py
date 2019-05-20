from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.std.std import Std


class Data2DLayer(Layer):

    def __init__(self, name, data):
        Layer.__init__(self, name)
        self.data = data


    def paint(self, painter, option, widget):
        painter.setPen(QColor(0, 0, 0, 255))
        
        ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT

        radius = 3

        for point in self.data:
            pos_x = (point[0] - radius)*ratio_x
            pos_y = (point[1] - radius)*ratio_y

            painter.drawEllipse(pos_x, pos_y, 2*radius*ratio_x, 2*radius*ratio_x)