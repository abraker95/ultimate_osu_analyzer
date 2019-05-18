from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.pos import Pos
from osu.local.hitobject.mania.mania_holdnote_hitobject import ManiaHoldNoteHitobject


class ManiaHoldNoteIO():

    @staticmethod
    def load_holdnote(data, difficulty):
        holdnote = ManiaHoldNoteHitobject()
        if not data: return holdnote

        ManiaHoldNoteIO.__process_holdnote_data(data, holdnote, difficulty)

        return holdnote


    @staticmethod
    def __process_holdnote_data(data, holdnote, difficulty):
        holdnote.pos            = Pos(int(data[0]), int(data[1]))
        holdnote.time           = int(data[2])
        holdnote.hitobject_type = int(data[3])
        
        slider_data = data[5].split(':')
        holdnote.end_time = int(slider_data[0])

        holdnote.difficulty = difficulty