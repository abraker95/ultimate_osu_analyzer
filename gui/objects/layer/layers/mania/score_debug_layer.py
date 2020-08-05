from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import numpy as np

from analysis.osu.mania.map_data import ManiaMapData
from analysis.osu.mania.score_data import ManiaScoreData

from misc.math_utils import *
from generic.temporal import Temporal
from gui.objects.layer.layer import Layer

from osu.local.hitobject.mania.mania import Mania, ManiaSettings
from analysis.osu.mania.action_data import ManiaActionData



class ManiaScoreDebugLayer(Layer, Temporal):

    def __init__(self, data, time_updater):
        Layer.__init__(self, 'Score debug layer')
        Temporal.__init__(self)

        beatmap, replay = data
        
        self.map_data = ManiaMapData.get_hitobject_data(beatmap.hitobjects)
        self.columns  = len(self.map_data)

        self.replay_data = ManiaActionData.get_replay_data(replay.play_data, self.columns)
        self.score_data  = ManiaScoreData.get_score_data(self.replay_data, self.map_data)

        time_updater.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())

        ManiaSettings.set_viewable_time_interval.connect(self.layer_changed)


    def paint(self, painter, option, widget):
        if not self.time: return
        if len(self.score_data) <= 0: return
        
        painter.setPen(QColor(255, 0, 0, 255))

        space_data   = widget.width(), widget.height(), self.columns, self.time
        spatial_data = ManiaSettings.get_spatial_data(*space_data)

        start_time, end_time = spatial_data[0], spatial_data[1]

        for column in range(self.columns):
            start_idx = find(self.score_data[column][:,0], start_time)
            end_idx   = find(self.score_data[column][:,0], end_time)
            end_idx   = min(end_idx + 1, len(self.score_data[column]))

            for score in self.score_data[column][start_idx:end_idx]:
                time   = score[0]
                column = score[1] 
                offset = score[2]

                pos_x, pos_y, scaled_note_width, scaled_note_height = self.get_draw_data(*spatial_data[2:], column, time + offset, time + offset)
                painter.drawText(int(pos_x), int(pos_y), str(offset))


    def get_draw_data(self, ratio_x, ratio_y, ratio_t, x_offset, y_offset, column, press_time, release_time):
        scaled_note_width  = ManiaSettings.note_width*ratio_x
        scaled_note_height = (release_time - press_time)*ratio_t

        pos_x = x_offset + column*(ManiaSettings.note_width + ManiaSettings.note_seperation)*ratio_x
        pos_y = y_offset + (self.time - press_time)*ratio_t - scaled_note_height

        return pos_x, pos_y, scaled_note_width, scaled_note_height
