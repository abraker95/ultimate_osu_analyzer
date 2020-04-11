import numpy as np

from misc.geometry import *
from misc.numpy_utils import NumpyUtils

from osu.local.beatmap.beatmap import Beatmap
from analysis.osu.mania.map_data import ManiaMapData
from analysis.osu.mania.action_data import ManiaActionData



class ManiaMapMetrics():

    """
    Raw metrics
    """
    @staticmethod
    def calc_press_rate(action_data, window_ms=1000):
        """
        Calculates presses per second across all columns within indicated ``window_ms`` of time

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaMapData.get_action_data``

        window_ms : int
            Duration in milliseconds for which actions are counted up

        Returns
        -------
        (numpy.array, numpy.array)
        Tuple of ``(times, aps)``. ``times`` are timings corresponding to recorded actions per second. 
            ``aps`` are actions per second at indicated time.
        """
        aps = []
        for i in range(len(action_data)):
            actions_in_range = ManiaActionData.get_actions_between(action_data, action_data[i, 0] - window_ms, action_data[i, 0])
            num_actions = ManiaActionData.count_actions(actions_in_range, ManiaActionData.PRESS)
            aps.append([ action_data[i, 0], 1000*num_actions/window_ms ])

        return np.asarray(aps)


    @staticmethod
    def calc_press_rate_col(action_data, col, window_ms=1000):
        """
        Calculates presses per second in the specified column within indicated ``window_ms`` of time

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaMapData.get_action_data``

        col : int
            Column to calculated presses per second for

        window_ms : int
            Duration in milliseconds for which actions are counted up

        Returns
        -------
        (numpy.array, numpy.array)
        Tuple of ``(times, aps)``. ``times`` are timings corresponding to recorded actions per second. 
            ``aps`` are actions per second at indicated time.
        """
        action_data = action_data[:, [0, col]]
        aps = []

        for i in range(len(action_data)):
            actions_in_range = ManiaActionData.get_actions_between(action_data, action_data[i, 0] - window_ms, action_data[i, 0])
            num_actions = ManiaActionData.count_actions(actions_in_range, ManiaActionData.PRESS)
            aps.append([ action_data[i, 0], 1000*num_actions/window_ms ])

        return np.asarray(aps)


    @staticmethod
    def calc_max_press_rate_per_col(action_data, window_ms=1000):
        """
        Takes which column has max presses per second within indicated ``window_ms`` of time

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaMapData.get_action_data``

        window_ms : int
            Duration in milliseconds for which actions are counted up

        Returns
        -------
        (numpy.array, numpy.array)
        Tuple of ``(times, max_aps_per_col)``. ``times`` are timings corresponding to recorded actions per second. 
            ``max_aps_per_col`` are max actions per second at indicated time.
        """
        keys = ManiaActionData.num_keys(action_data)
        max_aps_per_col = []

        for i in range(len(action_data)):
            aps_col = []
            for col in range(1, keys + 1):
                col_data = action_data[:, [0, col]]

                actions_in_range = ManiaActionData.get_actions_between(col_data, col_data[i, 0] - window_ms, col_data[i, 0])
                num_actions = ManiaActionData.count_actions(actions_in_range, ManiaActionData.PRESS)
                aps_col.append(1000*num_actions/window_ms)
            
            max_aps_per_col.append([ action_data[i, 0], max(aps_col) ])

        return np.asarray(max_aps_per_col)


    @staticmethod
    def detect_chords(action_data):
        """
        Masks note that are detected as chords

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        numpy.array
        action_data mask of actions detected that correspond to chord patterns. 1 if chord pattern 0 otherwise
        """
        chord_mask = action_data[:]
        chord_mask[:, 1:][chord_mask[:, 1:] == ManiaMapData.RELEASE] = 0  # Remove Releases
        chord_mask[:, 1:][chord_mask[:, 1:] == ManiaMapData.HOLD]    = 0  # Remove Holds

        # If not matching chord, set to 0
        for action in chord_mask:
            presses = action[1:][action[1:] == ManiaMapData.PRESS]
            if len(presses) < 3: action[1:][action[1:] == ManiaMapData.PRESS] = 0

        return chord_mask

        start_times = ManiaMapData.start_times(hitobject_data, column)
        if len(start_times) < 2: return [], []
    
        return start_times[1:], np.diff(start_times)


    @staticmethod
    def calc_notes_per_sec(hitobject_data, column=None):
        """
        Gets average note rate with window of 1 second throughout the beatmap in the specified ``column``

        Parameters
        ----------
        hitobject_data : numpy.array
            Hitobject data from ``ManiaMapData.get_hitobject_data``

        column : int
            Which column number to get average note rate for. If left blank, interprets all columns as one.

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(start_times, notes_per_sec)``. ``start_times`` are timings corresponding to start of notes. 
            ``notes_per_sec`` are average note rates at ``start_times`` point in time. Resultant array size is 
            ``len(hitobject_data) - 1``.
        """
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
        
