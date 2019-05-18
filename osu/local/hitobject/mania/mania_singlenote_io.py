import math

from misc.pos import Pos
from osu.local.hitobject.mania.mania_singlenote_hitobject import ManiaSingleNoteHitobject


class ManiaSingleNoteIO():

    @staticmethod
    def load_singlenote(data, difficulty):
        singlenote = ManiaSingleNoteHitobject()
        if not data: return singlenote

        ManiaSingleNoteIO.__process_hitobject_data(data, singlenote, difficulty)

        return singlenote


    @staticmethod
    def get_data(self, singlenote):
        # TODO
        pass


    @staticmethod
    def __process_hitobject_data(data, singlenote, difficulty):
        singlenote.pos            = Pos(int(data[0]), int(data[1]))
        singlenote.time           = int(data[2])
        singlenote.hitobject_type = int(data[3])

        singlenote.difficulty     = difficulty