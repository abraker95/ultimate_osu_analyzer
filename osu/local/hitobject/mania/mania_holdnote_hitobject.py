from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.hitobject import Hitobject
from osu.local.beatmap.beatmap_utility import BeatmapUtil

from misc.frozen_cls import FrozenCls



@FrozenCls
class ManiaHoldNoteHitobject(QGraphicsItem, Hitobject):

    def __init__(self):
        self.end_time   = None

        QGraphicsItem.__init__(self)
        Hitobject.__init__(self)


    def paint(self, painter, option, widget):
        # TODO
        pass


    def resizeEvent(self, event):
        print('owh')


    def boundingRect(self):
        return QRectF(0, 0, self.radius, self.radius)