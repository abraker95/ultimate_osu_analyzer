import numpy as np

from osu.local.beatmap.beatmap_utility import BeatmapUtil
from misc.numpy_utils import NumpyUtils



class MapData():

    TIME = 0
    POS  = 1

    @staticmethod
    def get_data_before(hitobject_data, time):
        idx_time = hitobject_data.get_idx_start_time(time)

        if not idx_time: return None
        if idx_time < 1: return None

        return hitobject_data.hitobject_data[idx_time - 1][-1]


    @staticmethod
    def get_data_after(hitobject_data, time):
        idx_time = hitobject_data.get_idx_end_time(time)
        
        if not idx_time:                       return None
        if idx_time > len(hitobject_data) - 2: return None
            
        return hitobject_data.hitobject_data[idx_time + 1][0]


    @staticmethod
    def time_slice(hitobject_data, start_time, end_time):
        start_idx = hitobject_data.get_idx_start_time(start_time)
        end_idx   = hitobject_data.get_idx_end_time(end_time)

        return hitobject_data.hitobject_data[start_idx:end_idx]


    '''
    [
        [ time, pos ],
        [ time, pos ],
        ... N fruits
    ]
    '''
    def __init__(self):
        self.set_data_raw([])


    def __len__(self):
        return len(self.hitobject_data)


    def set_data_hitobjects(self, hitobjects):
        self.hitobject_data = [ hitobject.raw_data() for hitobject in hitobjects ]
        return self


    def set_data_raw(self, raw_data):
        self.hitobject_data = raw_data
        return self


MapData.full_hitobject_data = MapData()