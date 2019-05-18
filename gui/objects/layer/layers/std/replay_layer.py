from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.std.std import Std


class ReplayLayer(Layer, Temporal):

    def __init__(self, data, time_driver):
        Layer.__init__(self, 'Hitobject outlines')
        Temporal.__init__(self)

        self.replay = data

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def paint(self, painter, option, widget):
        if not self.time: return
        painter.setPen(QColor(0, 200, 0, 255))
        
        ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT

        data  = self.replay.get_data_at_time(self.time)
        pos_x = data.x*ratio_x
        pos_y = data.y*ratio_y

        painter.drawEllipse(pos_x, pos_y, 3, 3)