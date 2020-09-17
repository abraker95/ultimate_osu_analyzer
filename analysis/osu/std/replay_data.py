import numpy as np
import pandas as pd
import itertools
import time

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
            k1_pressed    = ((replay_event.keys_pressed & k1_mask) > 0)
            k2_pressed    = ((replay_event.keys_pressed & k2_mask) > 0) 
            m1_pressed    = ((replay_event.keys_pressed & m1_mask) > 0)
            m2_pressed    = ((replay_event.keys_pressed & m2_mask) > 0)
            smoke_pressed = (replay_event.keys_pressed & smoke_mask) > 0

            is_key_hold = np.asarray([ m1_pressed, m2_pressed, k1_pressed, k2_pressed, smoke_pressed ])

            data = np.asarray([ StdReplayData.FREE for _ in range(5) ])
            data[~hold_state &  is_key_hold] = StdReplayData.PRESS
            data[ hold_state &  is_key_hold] = StdReplayData.HOLD
            data[ hold_state & ~is_key_hold] = StdReplayData.RELEASE

            # Handles autoplay key press & release occuring at same time
            replay_time = replay_event.t
            while replay_time in replay_data: replay_time +=1

            replay_data[replay_time] = [ replay_time, replay_event.x, replay_event.y ] + list(data)
            hold_state = is_key_hold

        replay_data = list(replay_data.values())
        replay_data.sort(key=lambda x: x[0])
        return pd.DataFrame(replay_data, columns=[ 'time', 'x', 'y', 'm1', 'm2', 'k1', 'k2', 'smoke' ])


    @staticmethod
    def __get_key_state(master_key_state, key_states, press_block=False, release_block=True):
        """
        Since std has 4 buttons that are essentially treat as one key,
        the 4 states need to be processed and merged into one state.

        Parameters
        ----------
        master_key_state : int
            The current state of the one merged key

        key_states : numpy.array
            The states of each individual key

        Returns
        -------
        int
            The resultant state of the master key
        """
        key_states = np.asarray(key_states)

        # If new state has a press
        if any(key_states == StdReplayData.PRESS):
            press_reg = True
            if press_block:  # Make sure player is not holding a key already
                press_reg &= master_key_state != StdReplayData.HOLD
            if press_reg:
                return StdReplayData.PRESS

        if any(key_states == StdReplayData.RELEASE):
            release_reg = True
            if release_block:  # Make sure player is not holding a key already
                release_reg = all(key_states != StdReplayData.HOLD)
            release_reg &= (master_key_state != StdReplayData.FREE) and (master_key_state != StdReplayData.RELEASE)
            if release_reg:
                return StdReplayData.RELEASE

        if (any(key_states == StdReplayData.HOLD) and (master_key_state != StdReplayData.RELEASE)) or (master_key_state == StdReplayData.HOLD):
            return StdReplayData.HOLD

        return StdReplayData.FREE


    @staticmethod
    def __reduce_replay_data(replay_data):
        not_free_mask = np.any(replay_data[['m1', 'm2', 'k1', 'k2']] != StdReplayData.FREE, 1).values
        
        filter_mask = np.full(len(replay_data), True)
        filter_mask[1:-1] = (not_free_mask[1:-1] | not_free_mask[:-2] | not_free_mask[2:])

        return replay_data.iloc[filter_mask]


    @staticmethod
    def get_reduced_replay_data(replay_data, press_block=True, release_block=False):
        """
        Filters out replay data where there are no buttons being pressed, except frames
        where button was pressed before or after the event. Removes smoke key, and merges
        4 buttons into one button

        Parameters
        ----------
        replay_data : numpy.array
            Action data from ``StdReplayData.get_replay_data``

        Returns
        -------
        numpy.array
        Reduced replay data
        """
        # Score data that will be filled in and returned
        new_data = {}

        # Number of things to loop through
        replay_data = StdReplayData.__reduce_replay_data(replay_data).values
        num_replay_events = len(replay_data)

        # replay pointer
        replay_idx = 0

        # Key state
        key_state = StdReplayData.FREE

        # Go through replay events
        while True:
            # Condition check whether all replay frames processed
            if replay_idx >= num_replay_events: break

            # Data for this event frame
            replay_time = replay_data[replay_idx][0]    # time
            replay_xpos = replay_data[replay_idx][1]    # x
            replay_ypos = replay_data[replay_idx][2]    # y
            replay_keys = replay_data[replay_idx][3:7]  # keys

            new_key_state = StdReplayData.__get_key_state(key_state, replay_keys, press_block, release_block)

            # Got all info at current index, now advance it
            replay_idx += 1

            if key_state != new_key_state:
                if key_state == StdReplayData.HOLD and new_key_state == StdReplayData.PRESS:
                    new_data[len(new_data)] = np.asarray([ replay_time - 1, replay_xpos, replay_ypos, StdReplayData.RELEASE ])

            # It's possible to trigger two PRESSES/RELEASES in a row if left/right keys happen to press/release one frame after another
            if key_state == StdReplayData.PRESS and new_key_state == StdReplayData.PRESS:
                # If we get two presses in a row, then it's effectively a HOLD
                key_state = StdReplayData.HOLD
                new_key_state = StdReplayData.HOLD
            else:
                key_state = new_key_state

            new_data[len(new_data)] = np.asarray([ replay_time, replay_xpos, replay_ypos, new_key_state ])

        # Convert recorded timings and states into a pandas data
        new_data = list(new_data.values())
        return pd.DataFrame(new_data, columns=[ 'time', 'x', 'y', 'k' ])


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
        return replay_data['time'][np.any(btn_data == StdReplayData.PRESS, 1)]


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
        return replay_data['time'][np.any(btn_data == StdReplayData.RELEASE, 1)]