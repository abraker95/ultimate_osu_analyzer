from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.std.std import Std


class ReplayLayer(Layer, Temporal):

    def __init__(self, data, time_driver):
        Layer.__init__(self, 'Replay - ' + str(data.player_name))
        Temporal.__init__(self)

        self.replay = data

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def paint(self, painter, option, widget):
        if not self.time: return
        painter.setPen(QColor(0, 200, 0, 255))
        
        ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT
        radius  = 1.5

        data  = self.replay.get_data_at_time(self.time)
        pos_x = (data.x - radius)*ratio_x
        pos_y = (data.y - radius)*ratio_y

        painter.drawEllipse(pos_x, pos_y, 2*radius, 2*radius)