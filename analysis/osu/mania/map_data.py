import numpy as np

from osu.local.hitobject.mania.mania import Mania
from misc.numpy_utils import NumpyUtils



class ManiaMapData():

    START_TIME = 0
    END_TIME   = 1

    @staticmethod
    def get_hitobject_data(hitobjects):
        """
        [
            [  [ time_start, time_end ], [ time_start, time_end ], ... N notes in col ],
            [  [ time_start, time_end ], [ time_start, time_end ], ... N notes in col ],
            ... N col
        ]
        """
        hitobject_data = list([ [] for _ in range(len(hitobjects)) ])
        
        for column, column_hitobjects in zip(range(len(hitobjects)), hitobjects):
            for hitobject in column_hitobjects:
                hitobject_data[column].append([hitobject.time, hitobject.get_end_time()])

        return hitobject_data


    @staticmethod
    def start_times(hitobject_data, column=None):
        if column == None: return np.sort(np.asarray([ hitobject[ManiaMapData.START_TIME] for column in hitobject_data for hitobject in column ]))
        else:              return np.asarray([ hitobject[ManiaMapData.START_TIME] for hitobject in hitobject_data[column] ])


    @staticmethod
    def end_times(hitobject_data, column=None):
        if column == None: return np.sort(np.asarray([ hitobject[ManiaMapData.END_TIME] for column in hitobject_data for hitobject in column ]))
        else:              return np.asarray([ hitobject[ManiaMapData.END_TIME] for hitobject in hitobject_data[column] ])


    @staticmethod
    def all_times(flat=True):
        # TODO
        if flat: return np.asarray([ ])
        else:    return [ ]


    @staticmethod
    def start_end_times(hitobject_data, column):
        return np.asarray(hitobject_data[column])


    @staticmethod
    def get_idx_start_time(hitobject_data, column, time):
        if not time: return None

        times = ManiaMapData.start_times(hitobject_data, column)
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))


    @staticmethod
    def get_idx_end_time(hitobject_data, column, time):
        if not time: return None

        times = ManiaMapData.end_times(hitobject_data, column)
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))