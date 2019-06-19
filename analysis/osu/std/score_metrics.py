from enum import Enum
import numpy as np
import scipy.stats

from misc.numpy_utils import NumpyUtils
from misc.geometry import get_distance
from misc.math_utils import prob_not, prob_and, prob_or

from analysis.osu.std.score_data import StdScoreData, StdScoreDataEnums


class StdScoreMetrics():

    """
    Takes arrays of score data pertaining to various players and transposes it to be an array of per-hitobject score data
    from various players

    [
        [
    a0      [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    a2      [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    aN      ...  N events
        ],
        [
    b0      [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    b1      [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    bN      ...  N events
        ],
        ...
    ]

    gets turned into

    [
        [
    a0      [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    b0      [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    N0      ...  N events
        ],
        [
    a1      [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    b1      [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    N1      ...  N events
        ],
        ...
    ]

    """
    @staticmethod
    def get_per_hitobject_score_data(score_data_array):
        return np.transpose(score_data_array, axes=(1, 0, 2))


    @staticmethod
    def get_percent_below_offset(per_hitobject_score_data, hitobject_idx, offset):
        hit_offsets = per_hitobject_score_data[hitobject_idx][:, StdScoreDataEnums.HIT_OFFSET.value]
        hit_offsets_below_offset = hit_offsets[abs(hit_offsets) < offset]

        return len(hit_offsets_below_offset)/len(hit_offsets)


    @staticmethod
    def trans_percent_players_taps(per_hitobject_score_data, offset):
        """
        Gives the percent of players tapping within the specified offset for each hitobject
        """
        times   = per_hitobject_score_data[:,0,0]
        percent = [ StdScoreMetrics.get_percent_below_offset(per_hitobject_score_data, i, offset) for i in range(len(per_hitobject_score_data)) ]

        return times, np.asarray(percent)


    @staticmethod
    def solve_for_hit_offset(per_hitobject_score_data, hitobject_idx, target_percent):
        """
        Solves for the tapping offset for the note that 50% of players are able to do
        """
        offset         = 0
        target_percent = min(max(0.0, target_percent), 1.0)
        curr_percent   = StdScoreMetrics.get_percent_below_offset(per_hitobject_score_data, hitobject_idx, offset)

        while curr_percent < target_percent:
            curr_percent = StdScoreMetrics.get_percent_below_offset(per_hitobject_score_data, hitobject_idx, offset)
            offset += 1

        return offset


    @staticmethod
    def trans_solve_for_hit_offset(per_hitobject_score_data):
        """
        Solves for the tapping offset for the note that 50% of players are able to do
        """
        times       = per_hitobject_score_data[:,0,0]
        hit_offsets = [ StdScoreMetrics.solve_for_hit_offset(per_hitobject_score_data, i, 0.5) for i in range(len(per_hitobject_score_data)) ]

        return times, np.asarray(hit_offsets)