from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.math_utils import *
from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.std.std import Std
from analysis.osu.std.replay_data import StdReplayData


class StdReplayHoldLayer(Layer, Temporal):

    viewable_time_interval = 1000   # ms

    def __init__(self, data, time_driver):
        self.replay     = data
        self.event_data = None

        Layer.__init__(self, 'Replay hold - ' + str(self.replay.player_name))
        Temporal.__init__(self)

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def paint(self, painter, option, widget):
        if not self.time: return

        if self.event_data == None:
            self.event_data = StdReplayData.get_event_data(self.replay.play_data)
        
        ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT
        radius  = 1.5

        start_idx = find(self.event_data, self.time - StdReplayHoldLayer.viewable_time_interval, selector=lambda event: event[StdReplayData.TIME])
        end_idx   = find(self.event_data, self.time, selector=lambda event: event[StdReplayData.TIME])
        end_idx   = min(end_idx + 1, len(self.event_data))

        for prev_event, curr_event in zip(self.event_data[start_idx:end_idx - 1], self.event_data[start_idx + 1:end_idx]):
            prev_pos_x, curr_pos_x = prev_event[StdReplayData.XPOS]*ratio_x, curr_event[StdReplayData.XPOS]*ratio_x
            prev_pos_y, curr_pos_y = prev_event[StdReplayData.YPOS]*ratio_y, curr_event[StdReplayData.YPOS]*ratio_y

            # K1 is always used with M1; K2 is always used with M2. So check for keys first, then mouse
            if   prev_event[StdReplayData.K1]: painter.setPen(QColor.fromHsl(32,  255, 128, 255))
            elif prev_event[StdReplayData.K2]: painter.setPen(QColor.fromHsl(180, 255, 96,  255))
            elif prev_event[StdReplayData.M1]: painter.setPen(QColor.fromHsl(0,   255, 128, 255))
            elif prev_event[StdReplayData.M2]: painter.setPen(QColor.fromHsl(120, 255, 96,  255))
            else:                              painter.setPen(QColor(0, 0, 0, 0))

            painter.drawLine(prev_pos_x, prev_pos_y, curr_pos_x, curr_pos_y)