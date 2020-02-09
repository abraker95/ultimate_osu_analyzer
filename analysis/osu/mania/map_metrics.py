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
    def calc_action_rate(action_data, window_ms=1000):
        """
        Calculates number of actions there are across all columns within indicated ``window_ms`` of time

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
        for start in range(len(action_data)):
            try: aps.append([ action_data[start, 0],  np.where(action_data[start, 0] + window_ms <= action_data[:, 0])[0][0] - start ])
            except IndexError: break

        return np.asarray(aps)


    @staticmethod
    def detect_chords(action_data):
        """
        Masks note that are detected as chords

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaMapData.get_action_data``

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