import math

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.math_utils import *
from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from osu.local.hitobject.mania.mania import Mania, ManiaSettings
from analysis.osu.mania.replay_data import ManiaReplayData


class ManiaHoldReplayLayer(Layer, Temporal):

    def __init__(self, data, time_driver):
        self.replay, self.columns = data
        self.columns = int(self.columns)
        
        self.event_data = None

        Layer.__init__(self, 'Hold times - ' + str(self.replay.player_name))
        Temporal.__init__(self)

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def paint(self, painter, option, widget):
        if not self.time: return
        painter.setPen(QPen(QColor(0, 50, 255, 120), 5))

        num_columns  = int(self.columns)
        space_data   = widget.width(), widget.height(), num_columns, self.time
        spatial_data = ManiaSettings.get_spatial_data(*space_data)

        start_time, end_time = spatial_data[0], spatial_data[1]
        
        if self.event_data == None:
            self.event_data = ManiaReplayData.get_replay_data(self.replay.play_data, self.columns)
        
        for column in range(self.columns):
            press_times = ManiaReplayData.start_times(self.event_data, column)

            start_idx = find(press_times, start_time)
            end_idx   = find(press_times, end_time)
            end_idx   = min(end_idx + 1, len(press_times))

            for event in self.event_data[column][start_idx : end_idx]:
                press_time, release_time = event
                pos_x, pos_y, scaled_note_width, scaled_note_height = self.get_draw_data(*spatial_data[2:], column, press_time, release_time)

                painter.fillRect(QRectF(pos_x, pos_y, scaled_note_width, scaled_note_height), QBrush(QColor(0, 50, 255, 120)))


    def get_draw_data(self, ratio_x, ratio_y, ratio_t, x_offset, y_offset, column, press_time, release_time):
        scaled_note_width  = ManiaSettings.note_width*ratio_x
        scaled_note_height = (release_time - press_time)*ratio_t

        pos_x = x_offset + column*(ManiaSettings.note_width + ManiaSettings.note_seperation)*ratio_x
        pos_y = y_offset + (self.time - press_time)*ratio_t - scaled_note_height

        return pos_x, pos_y, scaled_note_width, scaled_note_height