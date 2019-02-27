from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.beatmap.beatmap_utility import BeatmapUtil
from osu.local.playfield import Playfield


class OsuPlayField(Playfield):

    def __init__(self):
        Playfield.__init__(self)


    def set_time(self, time):
        self.time = time


    '''
    def get_visible_objects(self):
        hitcircles = []
        visible_hitobjects = BeatmapUtil.get_hitobjects_visible_at_time(self.modded_beatmap, self.time)
        return hitcircles
    '''