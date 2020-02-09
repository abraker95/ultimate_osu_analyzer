from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.mania.mania import Mania, ManiaSettings


class ManiaData2DLayer(Layer, Temporal):

    def __init__(self, name, columns, data, draw_func, time_driver):
        Layer.__init__(self, name)
        Temporal.__init__(self)

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())

        self.data      = data
        self.columns   = columns
        self.draw_func = draw_func

        ManiaSettings.set_note_height.connect(self.layer_changed)
        ManiaSettings.set_note_width.connect(self.layer_changed)
        ManiaSettings.set_note_seperation.connect(self.layer_changed)
        ManiaSettings.set_viewable_time_interval.connect(self.layer_changed)
        ManiaSettings.set_replay_opacity.connect(self.layer_changed)
       


    def paint(self, painter, option, widget):
        if not self.time: return
        painter.setPen(QColor(0, 0, 0, 255))

        space_data   = widget.width(), widget.height(), self.columns, self.time
        spatial_data = ManiaSettings.get_spatial_data(*space_data)

        try: self.draw_func(painter, self.columns, self.time, spatial_data, self.data)
        except Exception as e: print(e)