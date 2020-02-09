import numpy as np

from osu.local.hitobject.mania.mania import Mania
from misc.numpy_utils import NumpyUtils



class ManiaMapData():

    START_TIME = 0
    END_TIME   = 1

    FREE    = 0
    PRESS   = 1
    HOLD    = 2
    RELEASE = 3

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
                hitobject_data[column].append((hitobject.time, hitobject.get_end_time()))

        return hitobject_data


    @staticmethod
    def get_action_data(hitobjects, min_press_duration=50):
        """
        0 = Finger free float
        1 = Finger must impart force to press key
        2 = Finger must keep imparting force to keep key down
        3 = Finger must depart force to unpress key
        [
            [ time, col1_state, col2_state, ..., colN_state ],
            [ time, col1_state, col2_state, ..., colN_state ],
            [ time, col1_state, col2_state, ..., colN_state ],
            ... 
        ]
        """
        hitobject_data = ManiaMapData.get_hitobject_data(hitobjects)
        action_data = {}

        for col in range(len(hitobject_data)):
            for n in range(len(hitobject_data[col])):
                # Extract note timings
                note_start = hitobject_data[col][n][0]
                note_end   = hitobject_data[col][n][1]
                note_end   = note_end if (note_end - note_start >= min_press_duration) else (note_start + min_press_duration)

                # Record press state
                try:             action_data[note_start]
                except KeyError: action_data[note_start] = np.zeros(len(hitobject_data)) 
                action_data[note_start] += np.asarray([ ManiaMapData.PRESS if col==c else ManiaMapData.FREE for c in range(len(hitobject_data)) ])

                # Record release state
                try:             action_data[note_end]
                except KeyError: action_data[note_end] = np.zeros(len(hitobject_data))
                action_data[note_end] += np.asarray([ ManiaMapData.RELEASE if col==c else ManiaMapData.FREE for c in range(len(hitobject_data)) ])

        # Convert the dictionary of recorded timings and states into a sorted numpy array
        action_data = np.asarray([ np.concatenate(([timing], action_data[timing])) for timing in np.sort(list(action_data.keys())) ])
        
        # Record hold state
        for col in range(action_data.shape[1]):
            for i in range(1, len(action_data[:,col])):
                if (action_data[i - 1, col] == ManiaMapData.PRESS or action_data[i - 1, col] == ManiaMapData.HOLD) and action_data[i, col] != ManiaMapData.RELEASE:
                    action_data[i, col] = ManiaMapData.HOLD

        return action_data


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