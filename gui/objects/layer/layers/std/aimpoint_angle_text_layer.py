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


class AimpointAngleTextLayer(Layer, Temporal):

    def __init__(self, data, time_updater):
        Layer.__init__(self, 'Aimpoint angle text')
        
        beatmap = data
        map_data = StdMapData.get_aimpoint_data(beatmap.hitobjects)

        self.all_positions = StdMapData.all_positions(map_data)
        self.times, self.angles = StdMapMetrics.calc_angles(map_data)
        
        time_updater.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())

        StdSettings.set_view_time_back.connect(self.layer_changed)
        StdSettings.set_view_time_ahead.connect(self.layer_changed)


    def paint(self, painter, option, widget):
        if not self.time: return
        if len(self.all_positions) <= 0: return

        self.ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        self.ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT

        start_idx = find(self.times, self.time - StdSettings.view_time_back)
        end_idx   = find(self.times, self.time + StdSettings.view_time_ahead)
        end_idx   = min(end_idx + 1, len(self.times))

        painter.setPen(QColor(0, 0, 255, 255))
        for i in range(start_idx, end_idx):
            pos_x, pos_y = self.all_positions[i + 1]
            angle = self.angles[i]*180/math.pi

            painter.drawText(pos_x*self.ratio_x, pos_y*self.ratio_y, str(round(angle, 2)))
