from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.beatmap.beatmap_utility import BeatmapUtil


class ReplayLayer(Layer, Temporal):

    def __init__(self, data, time_driver):
        Layer.__init__(self, 'Hitobject outlines')
        Temporal.__init__(self)

        self.replay = data

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def area_resize_event(self, width, height):
        self.ratio_x = width/BeatmapUtil.PLAYFIELD_WIDTH
        self.ratio_y = height/BeatmapUtil.PLAYFIELD_HEIGHT


    def paint(self, painter, option, widget):
        if not self.time: return
        painter.setPen(QColor(0, 200, 0, 255))
        
        data  = self.replay.get_data_at_time(self.time)
        pos_x = data.x*self.ratio_x
        pos_y = data.y*self.ratio_y

        painter.drawEllipse(pos_x, pos_y, 3, 3)