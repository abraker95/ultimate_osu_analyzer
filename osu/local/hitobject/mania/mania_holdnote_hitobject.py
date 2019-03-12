from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.hitobject import Hitobject
from osu.local.beatmap.beatmap_utility import BeatmapUtil



class ManiaHoldNoteHitobject(QGraphicsItem, Hitobject):

    def __init__(self, hitobject_data):
        QGraphicsItem.__init__(self)
        Hitobject.__init__(self, hitobject_data)

        self.__process_holdnote_data(hitobject_data)


    def paint(self, painter, option, widget):
        # TODO
        pass


    def resizeEvent(self, event):
        print('owh')


    def boundingRect(self):
        return QRectF(0, 0, self.radius, self.radius)


    def __process_holdnote_data(self, hitobject_data):
        slider_data = hitobject_data[5].split(':')
        self.end_time = int(slider_data[0])
        return