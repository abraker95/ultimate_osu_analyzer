from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from analysis.map_metrics import MapMetrics
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

        aimpoints = BeatmapUtil.get_aimpoints_from_hitobjects(self.playfield.beatmap, self.playfield.visible_hitobjects)
        aimpoints = list(aimpoints)

        if len(aimpoints) < 1: return

        time, angles = MapMetrics.calc_angles(aimpoints)
        time, pos = zip(*aimpoints)

        painter.setPen(QColor(0, 0, 255, 255))
        for i in range(len(angles)):
            painter.drawText(pos[i + 1].x*self.ratio_x, pos[i + 1].y*self.ratio_y, str(round(angles[i]*180/math.pi, 2)))
