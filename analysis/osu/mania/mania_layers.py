from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.mania.mania import Mania, ManiaSettings
from analysis.osu.mania.action_data import ManiaActionData



def get_draw_data(ratio_x, ratio_y, ratio_t, x_offset, y_offset, column, time, event_time):
    scaled_note_width = ManiaSettings.note_width*ratio_x
    
    pos_x = x_offset + column*(ManiaSettings.note_width + ManiaSettings.note_seperation)*ratio_x
    pos_y = y_offset + (time - event_time)*ratio_t

    return pos_x, pos_y, scaled_note_width


class ManiaLayers():
    """
    Class used for time dependent visualization in central display.
    Sample use case: ``add_mania_layer('layer group', 'layer name', action_data, ManiaLayers.ManiaActionLayer)``
    """

    @staticmethod
    def ManiaActionLayer(painter, time, spatial_data, action_data, color=None, pen_width=5):
        start_time, end_time = spatial_data[0], spatial_data[1]
        action_data = action_data[(start_time <= action_data.index) & (action_data.index <= end_time)]

        for col in range(action_data.shape[1]):
            col_data = action_data[col]

            for i in range(len(col_data)):
                if col_data.iloc[i] == ManiaActionData.FREE:    continue
                if col_data.iloc[i] == ManiaActionData.PRESS:   painter.setPen(QPen(QColor(0,   150, 0,   100), pen_width))
                if col_data.iloc[i] == ManiaActionData.HOLD:    painter.setPen(QPen(QColor(255,   0, 255, 100), pen_width))
                if col_data.iloc[i] == ManiaActionData.RELEASE: painter.setPen(QPen(QColor(255, 255, 0,   100), pen_width))

                pos_x, pos_y, scaled_note_width = get_draw_data(*spatial_data[2:], col, time, col_data.index[i])
                painter.drawLine(pos_x, pos_y, pos_x + scaled_note_width, pos_y)


    @staticmethod
    def ManiaActionFillLayer(painter, time, spatial_data, action_data, color=QColor(0, 50, 255, 50), pen_width=1):
        start_time, end_time = spatial_data[0], spatial_data[1]
        brush = QBrush(color)

        for col in range(action_data.shape[1]):
            presses = action_data[col][action_data[col] == ManiaActionData.PRESS]
            releases = action_data[col][action_data[col] == ManiaActionData.RELEASE]

            # Get visible press and release ranges via index
            # because we need to also add one timing before start_time and one timing after end_time
            press_idx_start = presses[presses.index >= start_time]
            if len(press_idx_start) != 0: press_idx_start = presses.index.get_loc(press_idx_start.index[0])
            else: return

            press_idx_end = presses[presses.index <= end_time]
            if len(press_idx_end) != 0: press_idx_end = presses.index.get_loc(press_idx_end.index[-1]) + 1
            else: press_idx_end = press_idx_start + 1

            release_idx_start = releases[releases.index >= start_time]
            if len(release_idx_start) != 0: release_idx_start = releases.index.get_loc(release_idx_start.index[0])
            else: return

            release_idx_end = releases[releases.index <= end_time]
            if len(release_idx_end) != 0: release_idx_end = releases.index.get_loc(release_idx_end.index[-1]) + 1
            else: release_idx_end = release_idx_start + 1

            # Make sure presses and releases match up 1:1
            release_idx_start = min(release_idx_start, press_idx_start)
            press_idx_start = min(press_idx_start, release_idx_start)

            release_idx_end = max(release_idx_end, press_idx_end)
            press_idx_end = max(press_idx_end, release_idx_end)

            # Filter out timings to just what's needed
            press_times   = presses.iloc[press_idx_start : press_idx_end].index
            release_times = releases.iloc[release_idx_start : release_idx_end].index

            # Calculate geometry and draw
            for press_time, release_time in zip(press_times, release_times):
                pos_x_beg, pos_y_beg, scaled_note_width = get_draw_data(*spatial_data[2:], col, time, press_time)
                pos_x_end, pos_y_end, scaled_note_width = get_draw_data(*spatial_data[2:], col, time, release_time)

                height = max(ManiaSettings.note_height, pos_y_beg - pos_y_end)
                painter.fillRect(QRectF(pos_x_beg, pos_y_beg, scaled_note_width, -height), brush)


    @staticmethod
    def ManiaTextLayer(painter, time, spatial_data, action_data, pen_width=1):
        # TODO
        pass