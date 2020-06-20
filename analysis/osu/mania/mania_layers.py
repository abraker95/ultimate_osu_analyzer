from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import numpy as np

from misc.geometry import *
from misc.numpy_utils import NumpyUtils

from osu.local.hitobject.mania.mania import Mania, ManiaSettings

from analysis.osu.mania.map_data import ManiaMapData
from analysis.osu.mania.map_metrics import ManiaMapMetrics
from analysis.osu.mania.replay_data import ManiaReplayData
from analysis.osu.mania.action_data import ManiaActionData
from analysis.osu.mania.score_data import ManiaScoreData


def get_draw_data(ratio_x, ratio_y, ratio_t, x_offset, y_offset, column, time, event_time):
    scaled_note_width = ManiaSettings.note_width*ratio_x
    
    pos_x = x_offset + column*(ManiaSettings.note_width + ManiaSettings.note_seperation)*ratio_x
    pos_y = y_offset + (time - event_time)*ratio_t

    return pos_x, pos_y, scaled_note_width


class ManiaLayers():
    """
    Class used for time dependent visualization in central display.
    Sample use case: ``add_mania_layer('layer group', 'layer name', hitobject_data, ManiaLayers.ManiaNoteLayer)``
    """

    @staticmethod
    def ManiaActionLayer(painter, columns, time, spatial_data, action_data, pen_width=5):
        start_time, end_time = spatial_data[0], spatial_data[1]
        action_data = action_data[np.logical_and(start_time <= action_data[:,0], action_data[:,0] <= end_time)]

        for data in action_data:
            for col in range(1, len(data)):
                if data[col] == ManiaActionData.FREE:    continue
                if data[col] == ManiaActionData.PRESS:   painter.setPen(QPen(QColor(0,   150, 0,   255), pen_width))
                if data[col] == ManiaActionData.HOLD:    painter.setPen(QPen(QColor(255,   0, 255, 255), pen_width))
                if data[col] == ManiaActionData.RELEASE: painter.setPen(QPen(QColor(255, 255, 0,   255), pen_width))

                pos_x, pos_y, scaled_note_width = get_draw_data(*spatial_data[2:], col - 1, time, data[0])
                painter.drawLine(pos_x, pos_y, pos_x + scaled_note_width, pos_y)


    @staticmethod
    def ManiaActionFillLayer(painter, columns, time, spatial_data, action_data, pen_width=1):
        start_time, end_time = spatial_data[0], spatial_data[1]
        brush = QBrush(QColor(0, 50, 255, 50))

        for col in range(1, action_data.shape[1]):
            press_times   = action_data[action_data[:, col] == 1][:, 0]
            release_times = action_data[action_data[:, col] == 3][:, 0]

            # Get visible press and release ranges
            press_time_start = np.where(press_times >= start_time)[0]
            if len(press_time_start) != 0: press_time_start = press_time_start[0]
            else: return

            press_time_end = np.where(press_times <= end_time)[0]
            if len(press_time_end) != 0: press_time_end = press_time_end[-1] + 1
            else: press_time_end = press_time_start + 1

            release_time_start = np.where(release_times >= start_time)[0]
            if len(release_time_start) != 0: release_time_start = release_time_start[0]
            else: return

            release_time_end = np.where(release_times <= end_time)[0]
            if len(release_time_end) != 0: release_time_end = release_time_end[-1] + 1
            else: release_time_end = release_time_start + 1

            # Make sure presses and releases match up 1:1
            release_time_start = min(release_time_start, press_time_start)
            press_time_start = min(press_time_start, release_time_start)

            release_time_end = max(release_time_end, press_time_end)
            press_time_end = max(press_time_end, release_time_end)

            # Resolve to indices to timings
            press_times   = press_times[press_time_start : press_time_end]
            release_times = release_times[release_time_start : release_time_end]

            for i in range(len(press_times)):
                pos_x_beg, pos_y_beg, scaled_note_width = get_draw_data(*spatial_data[2:], col - 1, time, press_times[i])
                pos_x_end, pos_y_end, scaled_note_width = get_draw_data(*spatial_data[2:], col - 1, time, release_times[i])

                height = max(ManiaSettings.note_height, pos_y_beg - pos_y_end)
                painter.fillRect(QRectF(pos_x_beg, pos_y_beg, scaled_note_width, -height), brush)