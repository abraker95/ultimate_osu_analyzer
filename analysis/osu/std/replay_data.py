import numpy as np
import pandas as pd
import itertools

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.std.std import Std
from misc.numpy_utils import NumpyUtils



class StdReplayData():
    """
    Class used for navigating, extracting, and operating on standard gamemode replay data.
    
    .. note::
        This is not to be confused with the replay data in the osu.local.replay.replay.Replay class.
        Data used by this class is in numpy array form. Data in the Replay 
        class is based on *.osr file structure and is not in a friendly 
        format to perform analysis on.
    """

    FREE    = 0  # Finger free to float
    PRESS   = 1  # Finger must impart force to press key
    HOLD    = 2  # Finger must keep imparting force to keep key down
    RELEASE = 3  # Finger must depart force to unpress key

    @staticmethod 
    def get_replay_data(replay_events):
        """
        Gets replay data

        Parameters
        ----------
        replay_events : list
            Replay event data located in ``Replay.play_data``
        
        Returns
        -------
        numpy.array
            List of events with data on time, positions of cursor, and flags on 
            various key presses in the following format:
            ::
                [
                    [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
                    [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
                    [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
                    ...  N events
                ]
        """
        replay_data = {}

        # Previous state of whether finger is holding key down
        hold_state = np.asarray([ False for _ in range(5) ])

        m1_mask    = (1 << 0)
        m2_mask    = (1 << 1)
        k1_mask    = (1 << 2)
        k2_mask    = (1 << 3)
        smoke_mask = (1 << 4)

        for replay_event in replay_events:
            # "and not" because K1 is always used with M1; K2 is always used with M2. So make sure keys are not pressed along with mouse
            k1_pressed    = ((replay_event.keys_pressed & k1_mask) > 0)
            k2_pressed    = ((replay_event.keys_pressed & k2_mask) > 0) 
            m1_pressed    = ((replay_event.keys_pressed & m1_mask) > 0) and not k1_pressed
            m2_pressed    = ((replay_event.keys_pressed & m2_mask) > 0) and not k2_pressed
            smoke_pressed = (replay_event.keys_pressed & smoke_mask) > 0

            is_key_hold = np.asarray([ m1_pressed, m2_pressed, k1_pressed, k2_pressed, smoke_pressed ])

            data = np.asarray([ StdReplayData.FREE for _ in range(5) ])
            data[~hold_state &  is_key_hold] = StdReplayData.PRESS
            data[ hold_state &  is_key_hold] = StdReplayData.HOLD
            data[ hold_state & ~is_key_hold] = StdReplayData.RELEASE

            replay_data[replay_event.t] = [ replay_event.x, replay_event.y ] + list(data)
            hold_state = is_key_hold

        # Sort data by timings
        replay_data = dict(sorted(replay_data.items()))

        # Convert the dictionary of recorded timings and states into a pandas data
        replay_data = pd.DataFrame.from_dict(replay_data, orient='index', columns=['x', 'y', 'm1', 'm2', 'k1', 'k2', 'smoke'])
        replay_data.index.name = 'time'
        return replay_data


    @staticmethod
    def press_times(replay_data, btn=['m1', 'm2', 'k1', 'k2']):
        """
        Gets list of press timings in ``replay_data`` for button(s) ``btn``

        Parameters
        ----------
        replay_data : numpy.array
            Action data from ``StdReplayData.get_replay_data``

        btn : str, list
            Button(s) to get timings for
            Available options are: m1, m2, k1, k2, smoke

        Returns
        -------
        numpy.array
        Press timings
        """
        btn_data = replay_data[btn]
        return btn_data.index[np.any(btn_data == StdReplayData.PRESS, 1)]


    @staticmethod
    def release_times(replay_data, btn=['m1', 'm2', 'k1', 'k2']):
        """
        Gets list of release timings in ``replay_data`` for button(s) ``btn``

        Parameters
        ----------
        replay_data : numpy.array
            Action data from ``StdReplayData.get_replay_data``

        btn : str, list
            Button(s) to get timings for
            Available options are: m1, m2, k1, k2, smoke

        Returns
        -------
        numpy.array
        Release timings
        """
        btn_data = replay_data[btn]
        return btn_data.index[np.any(btn_data == StdReplayData.RELEASE, 1)]