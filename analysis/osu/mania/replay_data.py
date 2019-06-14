import numpy as np

from osu.local.hitobject.mania.mania import Mania
from misc.numpy_utils import NumpyUtils



'''
[
    [ (time_start, time_end), (time_start, time_end), (time_start, time_end), ... N events in col ],
    [ (time_start, time_end), (time_start, time_end), (time_start, time_end), ... N events in col ],
    ... N cols
]
'''
class ManiaReplayData():

    START_TIME = 0
    END_TIME   = 1

    @staticmethod
    def get_replay_data(replay_events, columns):
        event_data   = list([ [] for _ in range(columns) ])
        press_states = list([ None for _ in range(columns) ])

        for replay_event in replay_events:
            for column in range(columns):
                is_key_press = ((int(replay_event.x) & (1 << column)) > 0)

                if press_states[column] == None and is_key_press:
                    press_states[column] = replay_event.t

                if press_states[column] != None and not is_key_press:
                    event_data[column].append(np.asarray([ press_states[column], replay_event.t ]))
                    press_states[column] = None

        return event_data


    @staticmethod
    def start_times(event_data, column):
        return np.asarray([ event[ManiaReplayData.START_TIME] for event in event_data[column] ])


    @staticmethod
    def end_times(event_data, column):
        return np.asarray([ event[ManiaReplayData.END_TIME] for event in event_data[column] ])


    @staticmethod
    def all_times(flat=True):
        # TODO
        if flat: return np.asarray([ ])
        else:    return [ ]


    @staticmethod
    def start_end_times(event_data, column):
        return np.asarray(event_data[column])


    @staticmethod
    def get_idx_start_time(event_data, column, time):
        if not time: return None

        times = ManiaReplayData.start_times(event_data, column)
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))


    @staticmethod
    def get_idx_end_time(event_data, column, time):
        if not time: return None

        times = ManiaReplayData.end_times(event_data, column)
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))