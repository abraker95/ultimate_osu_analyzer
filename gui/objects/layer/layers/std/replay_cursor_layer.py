from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import numpy as np

from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.std.std import Std, StdSettings
from analysis.osu.std.replay_data import StdReplayData


class StdReplayCursorLayer(Layer, Temporal):

    def __init__(self, replay, time_driver):
        self.replay_data = StdReplayData.get_replay_data(replay.play_data)

        Layer.__init__(self, 'Replay cursor - ' + str(replay.player_name))
        Temporal.__init__(self)

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())

        StdSettings.set_cursor_radius.connect(self.layer_changed)
        StdSettings.set_cursor_thickness.connect(self.layer_changed)
        StdSettings.set_cursor_color.connect(self.layer_changed)


    def paint(self, painter, option, widget):
        if not self.time: return
        painter.setPen(QPen(StdSettings.cursor_color, StdSettings.cursor_thickness))
        
        ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT
        radius  = StdSettings.cursor_radius

        frame = self.replay_data[self.replay_data.index <= self.time].iloc[-1]        
        pos_x = (frame['x'] - radius)*ratio_x
        pos_y = (frame['y'] - radius)*ratio_y

        painter.drawEllipse(pos_x, pos_y, 2*radius, 2*radius)