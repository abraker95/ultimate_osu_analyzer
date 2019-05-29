import math

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.math_utils import *
from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.mania.mania import Mania, ManiaSettings


class ManiaRawReplayLayer(Layer, Temporal):

    def __init__(self, data, time_driver):
        self.replay, self.columns = data

        Layer.__init__(self, 'Raw replay - ' + str(self.replay.player_name))
        Temporal.__init__(self)

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def paint(self, painter, option, widget):
        if not self.time: return
        painter.setPen(QColor(0, 150, 0, 255))

        num_columns  = int(self.columns)
        space_data   = widget.width(), widget.height(), num_columns, self.time
        spatial_data = ManiaSettings.get_spatial_data(*space_data)

        start_time, end_time = spatial_data[0], spatial_data[1]

        start_idx = find(self.replay.play_data, start_time, selector=lambda event: event.t)
        end_idx   = find(self.replay.play_data, end_time,   selector=lambda event: event.t)
        end_idx   = min(end_idx + 1, len(self.replay.play_data))

        replay_events = self.replay.play_data[start_idx : end_idx]

        for replay_event in replay_events:
            for key_press in Mania.get_key_presses(replay_event.x):
                pos_x, pos_y, scaled_note_width = self.get_draw_data(*spatial_data[2:], key_press, replay_event.t)
                painter.drawLine(pos_x, pos_y, pos_x + scaled_note_width, pos_y)


    def get_draw_data(self, ratio_x, ratio_y, ratio_t, x_offset, y_offset, column, event_time):
        scaled_note_width  = ManiaSettings.note_width*ratio_x
        scaled_note_height = ManiaSettings.note_height*ratio_y

        pos_x = x_offset + column*(ManiaSettings.note_width + ManiaSettings.note_seperation)*ratio_x
        pos_y = y_offset + (self.time - event_time)*ratio_t

        return pos_x, pos_y, scaled_note_width