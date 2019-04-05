from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.objects.layer.layer import Layer
from osu.local.beatmap.beatmap_utility import *

from analysis.map_data import MapData, full_hitobject_data
from misc.pos import Pos
from misc.numpy_utils import NumpyUtils



class AimpointPathsLayer(Layer):

    def __init__(self, playfield):
        Layer.__init__(self, 'Aimpoint Paths')
        self.playfield = playfield


    def area_resize_event(self, width, height):
        self.ratio_x = width/BeatmapUtil.PLAYFIELD_WIDTH
        self.ratio_y = height/BeatmapUtil.PLAYFIELD_HEIGHT


    def paint(self, painter, option, widget):
        painter.setPen(QColor(255, 0, 0, 255))

        aimpoints = MapData().set_data_hitobjects(self.playfield.visible_hitobjects)
        aimpoints.append_to_start(MapData.get_data_before(full_hitobject_data, NumpyUtils.first(aimpoints.start_times())))
        aimpoints.append_to_end(MapData.get_data_after(full_hitobject_data, NumpyUtils.last(aimpoints.end_times())))
        
        aimpoints_positions = aimpoints.all_positions()

        for i in range(1, len(aimpoints_positions)):
            prev_pos, curr_pos = Pos(*aimpoints_positions[i - 1]), Pos(*aimpoints_positions[i])
            painter.drawLine(prev_pos.x*self.ratio_x, prev_pos.y*self.ratio_y, curr_pos.x*self.ratio_x, curr_pos.y*self.ratio_y)
