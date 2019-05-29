import math

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.math_utils import *
from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.mania.mania import Mania, ManiaSettings
from analysis.osu.mania.replay_data import ManiaReplayData


class ManiaReleaseReplayLayer(Layer, Temporal):

    def __init__(self, data, time_driver):
        self.replay, self.columns = data
        self.columns = int(self.columns)

        Layer.__init__(self, 'Release times - ' + str(self.replay.player_name))
        Temporal.__init__(self)

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def paint(self, painter, option, widget):
        if not self.time: return
        painter.setPen(QPen(QColor(0, 100, 255, 120), 5))

        num_columns  = int(self.columns)
        space_data   = widget.width(), widget.height(), num_columns, self.time
        spatial_data = ManiaSettings.get_spatial_data(*space_data)

        start_time, end_time = spatial_data[0], spatial_data[1]
        event_data = ManiaReplayData.get_replay_data(self.replay.play_data, self.columns)
        
        for column in range(self.columns):
            release_times = ManiaReplayData.end_times(event_data, column)

            start_idx = find(release_times, start_time)
            end_idx   = find(release_times, end_time)
            end_idx   = min(end_idx + 1, len(release_times))

            for press_time in release_times[start_idx : end_idx]:
                pos_x, pos_y, scaled_note_width = self.get_draw_data(*spatial_data[2:], column, press_time)
                painter.drawLine(pos_x, pos_y, pos_x + scaled_note_width, pos_y)


    def get_draw_data(self, ratio_x, ratio_y, ratio_t, x_offset, y_offset, column, event_time):
        scaled_note_width  = ManiaSettings.note_width*ratio_x

        pos_x = x_offset + column*(ManiaSettings.note_width + ManiaSettings.note_seperation)*ratio_x
        pos_y = y_offset + (self.time - event_time)*ratio_t

        return pos_x, pos_y, scaled_note_width