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
    """
    Class used for time dependent visualization in central display.
    Sample use case: ``add_std_layer('layer group', 'layer name', replay_data, StdLayers.StdReplayCursorLayer)``
    """
    @staticmethod
    def StdReplayCursorLayer(painter, ratio_x, ratio_y, time, replay_data):
        """
        Displays player's cursor movement in replays
        """
        radius  = StdSettings.cursor_radius

        try: frame = replay_data[replay_data['time'] <= time].iloc[-1]
        except IndexError: return

        pos_x = (frame['x'] - radius)*ratio_x
        pos_y = (frame['y'] - radius)*ratio_y

        painter.drawEllipse(pos_x, pos_y, 2*radius, 2*radius)


    @staticmethod
    def StdReplayScatterLayer(painter, ratio_x, ratio_y, time, replay_data, color=[0, 0, 0, 255]):
        """
        Displays held keys in replay
        """
        start_time  = time - StdSettings.view_time_back
        end_time    = time + StdSettings.view_time_ahead
        replay_data = replay_data[(start_time <= replay_data['time']) & (replay_data['time'] <= end_time)]

        radius = StdSettings.cursor_radius
        painter.setPen(QColor(*color))

        for prev_event, curr_event in zip(replay_data.iloc[:-1].iterrows(), replay_data.iloc[1:].iterrows()):
            _, prev_event = prev_event
            _, curr_event = curr_event

            curr_pos_x = curr_event['x']*ratio_x
            curr_pos_y = curr_event['y']*ratio_y

            painter.drawEllipse(curr_pos_x, curr_pos_y, 2*radius, 2*radius)


    @staticmethod
    def StdReplayHoldLayer(painter, ratio_x, ratio_y, time, replay_data):
        """
        Displays held keys in replay
        """
        start_time  = time - StdSettings.view_time_back
        end_time    = time + StdSettings.view_time_ahead
        replay_data = replay_data[(start_time <= replay_data['time']) & (replay_data['time'] <= end_time)]

        for prev_event, curr_event in zip(replay_data.iloc[:-1].iterrows(), replay_data.iloc[1:].iterrows()):
            _, prev_event = prev_event
            _, curr_event = curr_event

            prev_pos_x, curr_pos_x = prev_event['x']*ratio_x, curr_event['x']*ratio_x
            prev_pos_y, curr_pos_y = prev_event['y']*ratio_y, curr_event['y']*ratio_y

            if   prev_event['k1'] != 0: painter.setPen(StdSettings.k1_color)
            elif prev_event['k2'] != 0: painter.setPen(StdSettings.k2_color)
            elif prev_event['m1'] != 0: painter.setPen(StdSettings.m1_color)
            elif prev_event['m2'] != 0: painter.setPen(StdSettings.m2_color)
            else:                       painter.setPen(QColor(0, 0, 0, 0))

            painter.drawLine(prev_pos_x, prev_pos_y, curr_pos_x, curr_pos_y)


    @staticmethod
    def StdReplayCursorVel(painter, ratio_x, ratio_y, time, replay_data):
        """
        Displays cursor vel for replay in top left corner
        """
        t, vel = StdReplayMetrics.cursor_velocity(replay_data)
        idx = np.where(t > time)[0][0]

        painter.setPen(QColor(255, 0, 0, 255))
        painter.drawText(0, 10, f'{vel[idx]}')


    @staticmethod
    def StdScoreDebugLayer(painter, ratio_x, ratio_y, time, score_data):
        """
        Displays tap offset and position offset for each tapped note in replay.
        """
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