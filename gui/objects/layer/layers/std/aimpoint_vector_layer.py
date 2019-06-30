from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.map_metrics import StdMapMetrics

from osu.local.hitobject.std.std import Std, StdSettings

from misc.math_utils import *
from misc.numpy_utils import NumpyUtils

from generic.temporal import Temporal
from gui.objects.layer.layer import Layer



class AimpointVectorLayer(Layer, Temporal):

    def __init__(self, data, time_updater):
        Layer.__init__(self, 'Aimpoint vectors')
        Temporal.__init__(self)

        beatmap = data
        map_data = StdMapData.get_aimpoint_data(beatmap.hitobjects)

        self.all_positions = StdMapData.all_positions(map_data)
        self.forw_times, self.forw_vecs = StdMapMetrics.calc_forward_vel_vectors(map_data)
        self.back_times, self.back_vecs = StdMapMetrics.calc_backward_vel_vectors(map_data)
        
        time_updater.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())

        StdSettings.set_view_time_back.connect(self.layer_changed)
        StdSettings.set_view_time_ahead.connect(self.layer_changed)


    def paint(self, painter, option, widget):
        if not self.time: return
        if len(self.all_positions) <= 0: return

        self.ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        self.ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT

        start_idx = find(self.back_times, self.time - StdSettings.view_time_back)
        end_idx   = find(self.back_times, self.time + StdSettings.view_time_ahead)
        end_idx   = min(end_idx + 1, len(self.back_times))

        painter.setPen(QColor(255, 0, 0, 255))
        for i in range(start_idx, end_idx):
            pos_x, pos_y = self.all_positions[i + 1]
            vec_x, vec_y = self.back_vecs[i]*100

            painter.drawLine(pos_x*self.ratio_x, pos_y*self.ratio_y, (pos_x + vec_x)*self.ratio_x, (pos_y + vec_y)*self.ratio_y)

        painter.setPen(QColor(0, 0, 128, 255))
        for i in range(start_idx, end_idx):
            pos_x, pos_y = self.all_positions[i + 1]
            vec_x, vec_y = self.back_vecs[i]*100

            painter.drawLine(pos_x*self.ratio_x, pos_y*self.ratio_y, (pos_x - vec_x)*self.ratio_x, (pos_y - vec_y)*self.ratio_y)

        painter.setPen(QColor(0, 200, 0, 255))
        for i in range(start_idx, end_idx):
            pos_x, pos_y = self.all_positions[i + 1]
            vec_x, vec_y = self.forw_vecs[i + 1]*100

            painter.drawLine(pos_x*self.ratio_x, pos_y*self.ratio_y, (pos_x + vec_x)*self.ratio_x, (pos_y + vec_y)*self.ratio_y)