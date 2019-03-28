from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from analysis.map_metrics import MapMetrics
from gui.objects.layer.layer import Layer
from osu.local.beatmap.beatmap_utility import *



class AimpointVelocityTextLayer(Layer):

    def __init__(self, playfield):
        Layer.__init__(self, 'Aimpoint Velocity Text')
        self.playfield = playfield


    def area_resize_event(self, width, height):
        self.ratio_x = width/BeatmapUtil.PLAYFIELD_WIDTH
        self.ratio_y = height/BeatmapUtil.PLAYFIELD_HEIGHT


    def paint(self, painter, option, widget):
        painter.setPen(QColor(255, 0, 0, 255))

        aimpoints = BeatmapUtil.get_aimpoints_from_hitobjects(self.playfield.beatmap, self.playfield.visible_hitobjects)
        aimpoints = list(aimpoints)

        if len(aimpoints) < 1: return

        time, vel = MapMetrics.calc_velocity(aimpoints)
        time, pos = zip(*aimpoints)

        for i in range(1, len(aimpoints)):
            prev_pos, curr_pos = pos[i - 1], pos[i]
            midpoint = prev_pos.midpoint(curr_pos)

            painter.drawText(midpoint.x, midpoint.y, str(round(vel[i - 1], 2)))
