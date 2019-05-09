import math

from misc.pos import Pos
from osu.local.hitobject.std.std_singlenote_hitobject import StdSingleNoteHitobject


class StdSingleNoteIO():

    @staticmethod
    def load_singlenote(data):
        singlenote = StdSingleNoteHitobject()
        if not data: return singlenote

        StdSingleNoteIO.__process_hitobject_data(data, singlenote)

        return singlenote


    @staticmethod
    def get_data(self, singlenote):
        # TODO
        pass


    @staticmethod
    def __process_hitobject_data(data, singlenote):
        singlenote.pos            = Pos(int(data[0]), int(data[1]))
        singlenote.time           = int(data[2])
        singlenote.hitobject_type = int(data[3])