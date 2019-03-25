from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.objects.layer.layer import Layer
from osu.local.beatmap.beatmap_utility import *



class AimpointPathsLayer(Layer):

    def __init__(self, playfield):
        Layer.__init__(self, 'Aimpoint Paths')
        self.playfield = playfield


    def area_resize_event(self, width, height):
        self.ratio_x = width/BeatmapUtil.PLAYFIELD_WIDTH
        self.ratio_y = height/BeatmapUtil.PLAYFIELD_HEIGHT


    def paint(self, painter, option, widget):
        painter.setPen(QColor(255, 0, 0, 255))

        aimpoints = BeatmapUtil.get_aimpoints_from_hitobjects(self.playfield.beatmap, self.playfield.visible_hitobjects)
        aimpoints = list(aimpoints)

        if len(aimpoints) < 1: return
        aimpoint_times, aimpoints_positions = zip(*aimpoints)

        for i in range(1, len(aimpoints_positions)):
            prev_pos, curr_pos = aimpoints_positions[i - 1], aimpoints_positions[i]
            painter.drawLine(prev_pos.x*self.ratio_x, prev_pos.y*self.ratio_y, curr_pos.x*self.ratio_x, curr_pos.y*self.ratio_y)
