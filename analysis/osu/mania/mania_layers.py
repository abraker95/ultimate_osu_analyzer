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
    scaled_note_width  = ManiaSettings.note_width*ratio_x
    
    pos_x = x_offset + column*(ManiaSettings.note_width + ManiaSettings.note_seperation)*ratio_x
    pos_y = y_offset + (time - event_time)*ratio_t

    return pos_x, pos_y, scaled_note_width


class ManiaLayers():
    """
    Class used for time dependent visualization in central display.
    Sample use case: ``add_mania_layer('layer group', 'layer name', hitobject_data, ManiaLayers.ManiaNoteLayer)``
    """

    '''
    @staticmethod
    def ManiaNoteLayer(painter, spatial_data, time, hitobject_data):
        """
        Displays notes in map data
        """
        num_columns  = int(self.beatmap.difficulty.cs)
        space_data   = widget.width(), widget.height(), num_columns, self.time
        spatial_data = ManiaSettings.get_spatial_data(*space_data)

        start_time, end_time = spatial_data[0], spatial_data[1]

        for column in range(num_columns):
            start_idx = find(self.beatmap.hitobjects[column], start_time, selector=lambda hitobject: hitobject.time)
            end_idx   = find(self.beatmap.hitobjects[column], end_time,   selector=lambda hitobject: hitobject.get_end_time())

            visible_hitobjects = self.beatmap.hitobjects[column][start_idx : end_idx + 2]
            for visible_hitobject in visible_hitobjects:
                visible_hitobject.render_hitobject(painter, spatial_data[2:], self.time)
    '''

    @staticmethod
    def ManiaActionLayer(painter, columns, time, spatial_data, action_data):
        start_time, end_time = spatial_data[0], spatial_data[1]

        action_data = action_data[np.logical_and(start_time <= action_data[:,0], action_data[:,0] <= end_time)]
        for data in action_data:
            for col in range(1, len(data)):
                if data[col] == ManiaActionData.PRESS:   painter.setPen(QColor(0,   150, 0,   255))
                if data[col] == ManiaActionData.HOLD:    painter.setPen(QColor(255,   0, 255, 255))
                if data[col] == ManiaActionData.RELEASE: painter.setPen(QColor(255, 255, 0,   255))

                pos_x, pos_y, scaled_note_width = get_draw_data(*spatial_data[2:], col - 1, time, data[0])
                painter.drawLine(pos_x, pos_y, pos_x + scaled_note_width, pos_y)


    @staticmethod
    def ManiaChordLayer(painter, columns, time, spatial_data, chord_data):
        painter.setPen(QPen(QColor(0, 0, 200, 255), 5))

        start_time, end_time = spatial_data[0], spatial_data[1]
        print(columns)

        chord_data = chord_data[np.logical_and(start_time <= chord_data[:,0], chord_data[:,0] <= end_time)]
        for data in chord_data:
            for col in range(1, len(data)):
                if data[col] != 1: continue

                pos_x, pos_y, scaled_note_width = get_draw_data(*spatial_data[2:], col - 1, time, data[0])
                painter.drawLine(pos_x, pos_y, pos_x + scaled_note_width, pos_y)
        