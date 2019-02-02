from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.beatmap.beatmap_utility import BeatmapUtil



class OsuPlayField(QWidget):

    def __init__(self, beatmap):
        super().__init__()
        self.beatmap = beatmap
        self.time = 0


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        self.drawPoints(qp)

        qp.end()


    def set_time(self, time):
        self.time = time


    def drawPoints(self, qp):
      
        qp.setPen(Qt.red)
        size = self.size()
        
        for hitobject in self.beatmap.hitobjects:
            x_ratio = self.width()/BeatmapUtil.PLAYFIELD_WIDTH
            y_ratio = self.height()/BeatmapUtil.PLAYFIELD_HEIGHT
            qp.drawEllipse(hitobject.pos.x*x_ratio, hitobject.pos.y*y_ratio, self.beatmap.get_cs_px(), self.beatmap.get_cs_px())