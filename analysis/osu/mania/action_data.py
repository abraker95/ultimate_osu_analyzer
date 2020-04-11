import math
import numpy as np

from analysis.osu.mania.map_data import ManiaMapData
from osu.local.hitobject.mania.mania import Mania
from misc.numpy_utils import NumpyUtils


class ManiaActionData():

    FREE    = 0
    PRESS   = 1
    HOLD    = 2
    RELEASE = 3

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
        # It's easier to deal with start and end timings
        hitobject_data = ManiaMapData.get_hitobject_data(hitobjects)

        # Record data via dictionary to identify timings
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
                action_data[note_start] += np.asarray([ ManiaActionData.PRESS if col==c else ManiaActionData.FREE for c in range(len(hitobject_data)) ])

                # Record release state
                try:             action_data[note_end]
                except KeyError: action_data[note_end] = np.zeros(len(hitobject_data))
                action_data[note_end] += np.asarray([ ManiaActionData.RELEASE if col==c else ManiaActionData.FREE for c in range(len(hitobject_data)) ])

        # Convert the dictionary of recorded timings and states into a sorted numpy array
        action_data = np.asarray([ np.concatenate(([timing], action_data[timing])) for timing in np.sort(list(action_data.keys())) ])
        
        # Fill in hold states
        for col in range(action_data.shape[1]):
            for i in range(1, len(action_data[:,col]) - 1):
                # Every press must have a release, so if there is no RELEASE after a press then it muct be a hold
                press_with_no_hold = (action_data[i - 1, col] == ManiaActionData.PRESS) and (action_data[i, col] != ManiaActionData.RELEASE)

                # If there is a FREE after a HOLD and the current state is not a RELEASE, then it must be a continuing HOLD
                hold_continue = (action_data[i - 1, col] == ManiaActionData.HOLD) and (action_data[i, col] != ManiaActionData.RELEASE)
                
                if press_with_no_hold or hold_continue:
                    action_data[i, col] = ManiaActionData.HOLD

        return action_data


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
        return action_data.shape[1] - 1


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
        keys = action_data.shape[1] - 1
        left_half  = math.ceil(keys/2)  if left_handed else math.floor(keys/2)
        right_half = math.floor(keys/2) if left_handed else math.ceil(keys/2)

        left  = np.zeros((action_data.shape[0], left_half + 1))
        right = np.zeros((action_data.shape[0], right_half + 1))

        left[:, 0]  = action_data[:, 0]
        right[:, 0] = action_data[:, 0]

        left[:, 1:]  = action_data[:, 1:left_half + 1]
        right[:, 1:] = action_data[:, left_half + 1:]

        return (left, right)

    
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
        masked_action_data = np.zeros(action_data.shape)
        masked_action_data[:, 0] = action_data[:, 0]
        masked_action_data[:, 1:][np.isin(action_data[:, 1:], actions)] = 1
        masked_action_data = masked_action_data[index_start : index_end]

        if filter_free:
            masked_action_data = masked_action_data[masked_action_data[:, 1:].any(axis=1)]

        return masked_action_data


    @staticmethod
    def count_actions(action_data, actions, index_start=None, index_end=None):
        """
        Gets number of specified ``actions`` between ``index_start`` and ``index_end`` per entry.

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


    @staticmethod
    def get_actions_between(action_data, ms_start, ms_end, inclusive=True):
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

        inclusive : bool
            Flag indicating whether range is inclusive or exclusive. Inclusive by default.

        Returns
        -------
        numpy.array
        ``action_data`` slice of data between the times specified
        """
        if inclusive: return action_data[np.logical_and(action_data[:, 0] <= ms_end, action_data[:, 0] >= ms_start)]
        else:         return action_data[np.logical_and(action_data[:, 0] <  ms_end, action_data[:, 0] >  ms_start)]


    @staticmethod
    def is_action(action_data, index_start, index_end, actions, columns):
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
        column_mask = np.isin(np.arange(action_data.shape[1]), columns)
        return np.any(np.isin(action_data[index_start:, column_mask], actions))


    @staticmethod
    def idx_next_action(action_data, index_start, actions, columns):
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
        column_mask = np.isin(np.arange(action_data.shape[1]), columns)
        try: return np.where[np.isin(action_data[index_start:, column_mask], actions)][0][0] + index_start
        except IndexError: return -1