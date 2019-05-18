import math

from misc.pos import Pos
from osu.local.hitobject.std.std_spinner_hitobject import StdSpinnerHitobject


class StdSpinnerIO():

    @staticmethod
    def load_spinner(data, difficulty):
        spinner = StdSpinnerHitobject()
        if not data: return spinner

        StdSpinnerIO.__process_hitobject_data(data, spinner, difficulty)

        return spinner


    @staticmethod
    def get_data(self, spinner):
        # TODO
        pass


    @staticmethod
    def __process_hitobject_data(data, spinner, difficulty):
        spinner.pos            = Pos(int(data[0]), int(data[1]))
        spinner.time           = int(data[2])
        spinner.hitobject_type = int(data[3])
        spinner.end_time       = int(data[5])

        spinner.difficulty     = difficulty