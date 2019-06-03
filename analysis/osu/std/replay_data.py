import numpy as np
import itertools

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.std.std import Std
from misc.numpy_utils import NumpyUtils



class StdReplayData():

    TIME  = 0
    XPOS  = 1
    YPOS  = 2
    M1    = 3
    M2    = 4
    K1    = 5
    K2    = 6
    SMOKE = 7

    '''
    [
        [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
        [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
        [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
        ...  N events
    ]
    '''
    @staticmethod 
    def get_event_data(replay_events):
        event_data = []

        m1_mask    = (1 << 0)
        m2_mask    = (1 << 1)
        k1_mask    = (1 << 2)
        k2_mask    = (1 << 3)
        smoke_mask = (1 << 4)

        for replay_event in replay_events:
            # "and not" because K1 is always used with M1; K2 is always used with M2. So check for keys first, then mouse
            m1_pressed    = ((replay_event.keys_pressed & m1_mask) > 0) and not ((replay_event.keys_pressed & k1_mask) > 0)
            m2_pressed    = ((replay_event.keys_pressed & m2_mask) > 0) and not ((replay_event.keys_pressed & k2_mask) > 0)
            k1_pressed    = ((replay_event.keys_pressed & k1_mask) > 0)
            k2_pressed    = ((replay_event.keys_pressed & k2_mask) > 0) 
            smoke_pressed = (replay_event.keys_pressed & smoke_mask) > 0

            event = [ replay_event.t, replay_event.x, replay_event.y, m1_pressed, m2_pressed, k1_pressed, k2_pressed, smoke_pressed ]
            event_data.append(event)

        return event_data


    @staticmethod
    def press_start_times(event_data, key=None):
        if key == None:
            # TODO
            return np.asarray([ ])
        else:
            # TODO
            return np.asarray([ ])


    @staticmethod
    def press_end_times(event_data, key=None):
        if key == None:
            # TODO
            return np.asarray([ ])
        else:
            # TODO
            return np.asarray([ ])

    
    @staticmethod
    def press_start_end_times(event_data, key=None):
        if key == None:
            # TODO
            return np.asarray([ ])
        else:
            # TODO
            return np.asarray([ ])

    
    @staticmethod
    def get_idx_press_start_time(event_data, time, key=None):
        if not time: return None

        times = StdReplayData.press_start_times(event_data, key)
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))


    @staticmethod
    def get_idx_press_end_time(event_data, key, time):
        if not time: return None

        times = StdReplayData.press_end_times(event_data, key)
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))