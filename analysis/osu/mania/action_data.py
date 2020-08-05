import math
import numpy as np
import pandas as pd

from analysis.osu.mania.map_data import ManiaMapData
from osu.local.hitobject.mania.mania import Mania
from misc.numpy_utils import NumpyUtils


class ManiaActionData():

    FREE    = 0  # Finger free to float
    PRESS   = 1  # Finger must impart force to press key
    HOLD    = 2  # Finger must keep imparting force to keep key down
    RELEASE = 3  # Finger must depart force to unpress key

    @staticmethod
    def get_map_data(hitobjects, min_press_duration=1):
        """
        [
            [ col1_state, col2_state, ..., colN_state ],
            [ col1_state, col2_state, ..., colN_state ],
            [ col1_state, col2_state, ..., colN_state ],
            ... 
        ]
        """
        # It's easier to deal with start and end timings
        hitobject_data = ManiaMapData.get_hitobject_data(hitobjects)
        num_columns = len(hitobject_data)

        # Record data via dictionary to identify unique timings
        action_data = {}

        for col in range(num_columns):
            for hitobject in hitobject_data[col]:
                # Extract note timings
                note_start = hitobject[0]
                note_end   = hitobject[1]

                # Adjust note ending based on whether it is single or hold note (determined via min_press_duration)
                note_end = note_end if (note_end - note_start >= min_press_duration) else (note_start + min_press_duration)

                # Record press state
                try:             action_data[note_start]
                except KeyError: action_data[note_start] = np.zeros(num_columns) 
                action_data[note_start] += np.asarray([ ManiaActionData.PRESS if col==c else ManiaActionData.FREE for c in range(num_columns) ])

                # Record release state
                try:             action_data[note_end]
                except KeyError: action_data[note_end] = np.zeros(num_columns)
                action_data[note_end] += np.asarray([ ManiaActionData.RELEASE if col==c else ManiaActionData.FREE for c in range(num_columns) ])

        # Sort data by timings
        action_data = dict(sorted(action_data.items()))

        # Convert the dictionary of recorded timings and states into a pandas data
        action_data = pd.DataFrame.from_dict(action_data, orient='index')

        # Fill in HOLD data
        ManiaActionData.fill_holds(action_data)

        return action_data


    @staticmethod
    def get_replay_data(replay_events, cols):
        """
        [
            [ col1_state, col2_state, ..., colN_state ],
            [ col1_state, col2_state, ..., colN_state ],
            [ col1_state, col2_state, ..., colN_state ],
            ... 
        ]
        """
        cols = int(cols)

        # Record data via dictionary to identify unique timings
        replay_data = {}

        # Previous state of whether finger is holding key down
        hold_state = np.asarray([ False for _ in range(cols) ])

        for replay_event in replay_events:
            is_key_hold = np.asarray([ ((int(replay_event.x) & (1 << col)) > 0) for col in range(cols) ])
            if np.equal(hold_state, is_key_hold).all():
                continue

            data = np.asarray([ ManiaActionData.FREE for _ in range(cols) ])
            data[~hold_state &  is_key_hold] = ManiaActionData.PRESS
            data[ hold_state &  is_key_hold] = ManiaActionData.HOLD
            data[ hold_state & ~is_key_hold] = ManiaActionData.RELEASE

            replay_data[replay_event.t] = data
            hold_state = is_key_hold

        # Sort data by timings
        replay_data = dict(sorted(replay_data.items()))

        # Convert the dictionary of recorded timings and states into a pandas data
        replay_data = pd.DataFrame.from_dict(replay_data, orient='index')

        return replay_data


    @staticmethod
    def num_keys(action_data):
        """
        Gets number of keys according to the given ``action_data``

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        int
        Number of keys
        """
        return action_data.shape[1]


    @staticmethod
    def press_times(action_data, col):
        """
        Gets list of press timings in ``action_data`` for column ``col``

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        col : int
            Column to get timings for

        Returns
        -------
        numpy.array
        Press timings
        """
        return action_data[col].index[action_data[col] == ManiaActionData.PRESS]
        

    @staticmethod
    def release_times(action_data, col):
        """
        Gets list of release timings in ``action_data`` for column ``col``

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        col : int
            Column to get timings for

        Returns
        -------
        numpy.array
        Release timings
        """
        return action_data[col].index[action_data[col] == ManiaActionData.RELEASE]


    @staticmethod
    def filter_free(action_data):
        """
        Removes timings that have no actions in any column (anything but FREE)

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        numpy.array
        Filtered ``action_data``
        """
        return action_data[~np.all(action_data == ManiaActionData.FREE, 1)]


    @staticmethod
    def fill_holds(action_data):
        """
        Fill hold press states where they need to be. For example, if there are FREE between
        where PRESS and RELEASE occur, those will be filled with HOLD

        Thanks: DeltaEpsilon#7787

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        numpy.array
        Filtered ``action_data``
        """
        data = action_data.values.T

        for col in range(len(data)):
            hold_flag = False

            for row in range(len(data[col])):
                elem = data[col, row]
                
                if hold_flag:
                    if elem == ManiaActionData.PRESS:
                        raise ValueError(f'Two consequtive hold starts: ({col}, {row})')
                    elif elem == ManiaActionData.RELEASE: 
                        hold_flag = False
                    elif elem == ManiaActionData.FREE: 
                        data[col, row] = ManiaActionData.HOLD
                else:
                    if elem == ManiaActionData.PRESS:
                        hold_flag = True
                    elif elem == ManiaActionData.RELEASE: 
                        raise ValueError(f'Hold ended before it started: ({col}, {row})')


    @staticmethod
    def split_by_hand(action_data, left_handed=True):
        """
        Splits ``action_data`` into left and right hands

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        left_handed : bool
            Whether to prefer spliting odd even keys for left hand or right hand.
            If ``True`` then left hand. If ``False`` then right hand.

        Returns
        -------
        (numpy.array, numpy.array)
        A tuple of ``action_data`` for left hand and right hand
        """
        keys = action_data.shape[1]
        left_half = math.ceil(keys/2) if left_handed else math.floor(keys/2)
        return action_data.loc[:, :left_half - 1], action_data.loc[:, left_half:]

    
    @staticmethod
    def mask_actions(action_data, actions, index_start=None, index_end=None, filter_free=False):
        """
        Masks ``action_data`` between ``index_start`` and ``index_end``.
        If ``filter_free`` is ``True``, then also filters out entries in the range where there are no actions occuring.

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        actions : list
            A list of actions which to mask

        index_start : int
            Starting index of data in action data in which to mask actions for. ``None`` by default.

        index_end : int
            Ending index of data in action data in which to mask actions for. ``None`` by default

        filter_free : bool
            A flag for determining whether to filter out entries where there are no actions occuring.
            Doesn't filter by default.

        Returns
        -------
        numpy.array
        ``masked_action_data`` mask of the actions specified
        """
        if type(actions) != list: actions = [ actions ]
        masked_action_data = action_data.loc[index_start : index_end].isin(actions)

        if filter_free:
            masked_action_data = ManiaActionData.filter_free(masked_action_data)

        return masked_action_data


    @staticmethod
    def count_actions(action_data, actions, index_start=None, index_end=None):
        """
        Gets number of specified ``actions`` between ``index_start`` and ``index_end`` throughout all timings.

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        index_start : int
            Starting index of data in action data in which to count number of actions for. ``None`` by default.

        index_end : int
            Ending index of data in action data in which to count number of actions for. ``None`` by default

        actions : list
            A list of actions which to count

        Returns
        -------
        int
        ``action_count`` Number of actions in data
        """
        action_mask = ManiaActionData.mask_actions(action_data, actions, index_start, index_end).to_numpy()
        return np.sum(action_mask)

    '''
    @staticmethod
    def count_actions_per_timing(action_data, actions, index_start=None, index_end=None):
        """
        Gets number of specified ``actions`` between ``index_start`` and ``index_end`` per timing.

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        index_start : int
            Starting index of data in action data in which to count number of actions for. ``None`` by default.

        index_end : int
            Ending index of data in action data in which to count number of actions for. ``None`` by default

        actions : list
            A list of actions which to count

        Returns
        -------
        numpy.array
        ``action_data_count`` Action data representing number of actions specified for each entry
        """
        action_mask = ManiaActionData.mask_actions(action_data, actions, index_start, index_end)
        
        count = np.zeros(action_mask[:, :2].shape)
        count[:, 0] = action_mask[:, 0]
        count[:, 1] = np.sum(count[:, 1:], axis=1)

        return count
    '''


    @staticmethod
    def get_actions_between(action_data, ms_start, ms_end):
        """
        Gets a slice of ``action_data`` between ``ms_start`` and ``ms_end``, inclusively

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        ms_start : int
            Starting time of milliseconds in action data in which to get actions for

        ms_end : int
            Ending time in milliseconds of data in action data in which to get actions for

        Returns
        -------
        numpy.array
        ``action_data`` slice of data between the times specified
        """
        return action_data.loc[ms_start : ms_end]


    @staticmethod
    def is_action_in(action_data, actions, columns, index_start=None, index_end=None):
        """
        Checks whether specied ``actions`` in ``columns`` exist in slice of ``action_data`` 
        between ``index_start`` and ``index_end``

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        index_start : int
            Starting index to look actions for

        index_start : int
            Ending index to look actions for

        actions : list
            A list of actions to look for

        columns : list
            A list of columns to look at, where first column is 1, second column is 2, etc

        Returns
        -------
        bool
        ``found_actions`` Whether the ``actions`` have been found
        """
        if type(columns) != list: columns = [ columns ]
        return np.any(ManiaActionData.mask_actions(action_data.loc[:, columns], actions, index_start, index_end))


    @staticmethod
    def idx_next_action(action_data, index_start, actions, columns=[]):
        """
        Gets the next index of where one of ``actions`` occurs in one of specified ``columns``

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        index_start : int
            Starting index to look next actions for

        actions : list
            A list of actions to look for

        columns : list
            A list of columns to look at, where first column is 1, second column is 2, etc

        Returns
        -------
        int
        ``idx`` index where the next action occurs. Returns -1 if there is no action found.
        """
        action_data = ManiaActionData.mask_actions(action_data.loc[:, columns], actions, index_start)
        masked_data = ManiaActionData.filter_free(action_data)
        
        try: return masked_data.index[0]
        except: return index_start