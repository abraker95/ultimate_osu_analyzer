from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from analysis.map_data import MapData, full_hitobject_data
from analysis.map_metrics import MapMetrics
from misc.pos import Pos
from misc.numpy_utils import NumpyUtils

from gui.objects.layer.layer import Layer
from osu.local.beatmap.beatmap_utility import *



class AimpointAngleTextLayer(Layer):

    def __init__(self, playfield):
        Layer.__init__(self, 'Aimpoint Angle  Text')
        self.playfield = playfield


    def area_resize_event(self, width, height):
        self.ratio_x = width/BeatmapUtil.PLAYFIELD_WIDTH
        self.ratio_y = height/BeatmapUtil.PLAYFIELD_HEIGHT


    def paint(self, painter, option, widget):
        painter.setPen(QColor(255, 0, 0, 255))

        aimpoints = MapData().set_data_hitobjects(self.playfield.visible_hitobjects)
        aimpoints.append_to_start(MapData.get_data_before(full_hitobject_data, NumpyUtils.first(aimpoints.start_times())))
        aimpoints.append_to_end(MapData.get_data_after(full_hitobject_data, NumpyUtils.last(aimpoints.end_times())))

        print(aimpoints)
        time, angles = MapMetrics.calc_angles(aimpoints)
        aimpoints_positions = aimpoints.all_positions()

        painter.setPen(QColor(0, 0, 255, 255))
        for i in range(len(angles)):
            pos = Pos(*aimpoints_positions[i + 1])
            painter.drawText(pos.x*self.ratio_x, pos.y*self.ratio_y, str(round(angles[i]*180/math.pi, 2)))
