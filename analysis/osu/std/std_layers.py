from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import numpy as np

from misc.geometry import *
from misc.numpy_utils import NumpyUtils

from osu.local.hitobject.std.std import Std, StdSettings

from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.map_metrics import StdMapMetrics
from analysis.osu.std.replay_data import StdReplayData
from analysis.osu.std.replay_metrics import StdReplayMetrics
from analysis.osu.std.score_data import StdScoreData
from analysis.osu.std.score_metrics import StdScoreMetrics


class StdLayers():

    @staticmethod
    def StdReplayCursorLayer(painter, ratio_x, ratio_y, time, replay_data):
        painter.setPen(QPen(StdSettings.cursor_color, StdSettings.cursor_thickness))
        radius = StdSettings.cursor_radius

        idx = StdReplayData.get_idx_time(replay_data, time)
        pos_x, pos_y = replay_data[idx][StdReplayData.XPOS], replay_data[idx][StdReplayData.YPOS]
        
        pos_x = (pos_x - radius)*ratio_x
        pos_y = (pos_y - radius)*ratio_y

        painter.drawEllipse(pos_x, pos_y, 2*radius, 2*radius)


    @staticmethod
    def StdReplayHoldLayer(painter, ratio_x, ratio_y, time, replay_data):
        start_idx = StdReplayData.get_idx_time(replay_data, time - StdSettings.view_time_back)
        end_idx   = StdReplayData.get_idx_time(replay_data, time + StdSettings.view_time_ahead)

        for prev_event, curr_event in zip(replay_data[start_idx:end_idx - 1], replay_data[start_idx + 1:end_idx]):
            prev_pos_x, curr_pos_x = prev_event[StdReplayData.XPOS]*ratio_x, curr_event[StdReplayData.XPOS]*ratio_x
            prev_pos_y, curr_pos_y = prev_event[StdReplayData.YPOS]*ratio_y, curr_event[StdReplayData.YPOS]*ratio_y

            if   prev_event[StdReplayData.K1]: painter.setPen(StdSettings.k1_color)
            elif prev_event[StdReplayData.K2]: painter.setPen(StdSettings.k2_color)
            elif prev_event[StdReplayData.M1]: painter.setPen(StdSettings.m1_color)
            elif prev_event[StdReplayData.M2]: painter.setPen(StdSettings.m2_color)
            else:                              painter.setPen(QColor(0, 0, 0, 0))

            painter.drawLine(prev_pos_x, prev_pos_y, curr_pos_x, curr_pos_y)


    @staticmethod
    def StdReplayCursorVel(painter, ratio_x, ratio_y, time, replay_data):
        t, vel = StdReplayMetrics.cursor_velocity(replay_data)
        idx = np.where(t > time)[0][0]

        painter.setPen(QColor(255, 0, 0, 255))
        painter.drawText(0, 10, f'{vel[idx]}')


    @staticmethod
    def StdScoreDebugLayer(painter, ratio_x, ratio_y, time, score_data):
        if len(score_data) <= 0: return
        painter.setPen(QColor(255, 0, 0, 255))

        start_idx = find(score_data, time - StdSettings.view_time_back, selector=lambda event: event[0])
        end_idx   = find(score_data, time + StdSettings.view_time_ahead, selector=lambda event: event[0])
        end_idx   = min(end_idx + 1, len(score_data))

        for score in score_data[start_idx:end_idx]:
            pos_x, pos_y = score[1]
            time_offset  = score[2]
            pos_offset   = score[3]

            painter.drawText(pos_x*ratio_x, pos_y*ratio_y, str(time_offset) + '  ' + str(pos_offset))