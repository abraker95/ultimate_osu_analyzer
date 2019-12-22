import numpy as np

from misc.geometry import *
from misc.numpy_utils import NumpyUtils

from osu.local.beatmap.beatmap import Beatmap

from analysis.osu.mania.map_data import ManiaMapData



class ManiaMapMetrics():

    """
    Raw metrics
    """
    @staticmethod
    def calc_tapping_intervals(hitobject_data, column):
        start_times = ManiaMapData.start_times(hitobject_data, column)
        if len(start_times) < 2: return [], []
    
        return start_times[1:], np.diff(start_times)


    @staticmethod
    def calc_notes_per_sec(hitobject_data, column=None):
        if column == None:
            start_times = ManiaMapData.start_times(hitobject_data)
            mask, filtered_start_times, processed_start_times = NumpyUtils.mania_chord_to_jack(start_times)

            if len(start_times) < 2: return [], []
            intervals = 1000/(processed_start_times[1:] - filtered_start_times[:-1])
        
            return start_times[mask == 0][1:], intervals
        else:
            start_times = ManiaMapData.start_times(hitobject_data, column)

            if len(start_times) < 2: return [], []
            intervals = 1000/np.diff(start_times)
        
            return start_times[1:], intervals