import numpy as np

from osu.local.beatmap.beatmap_utility import BeatmapUtil
from misc.numpy_utils import NumpyUtils



class MapData():

    TIME = 0

    '''
    [
        [  [ time_start, time_end ], [ time_start, time_end ], ... N notes in col ],
        [  [ time_start, time_end ], [ time_start, time_end ], ... N notes in col ],
        ... N col
    ]
    '''
    def __init__(self):
        self.set_data_raw([])


    def set_data_hitobjects(self, hitobjects):
        self.hitobject_data = [ hitobject.raw_data() for hitobject in hitobjects ]
        return self


    def set_data_raw(self, raw_data):
        self.hitobject_data = raw_data
        return self


    def start_times(self):
        # TODO
        return np.array([ ])


    def end_times(self):
        # TODO
        return np.array([ ])


    def all_times(self, flat=True):
        # TODO
        if flat: return np.array([ ])
        else:    return [ ]


    def start_end_times(self):
        # TODO
        all_times = self.all_times(flat=False)
        return [ ]


    def get_idx_start_time(self, time):
        # TODO
        return None


    def get_idx_end_time(self, time):
       # TODO
       return None

MapData.full_hitobject_data = MapData()