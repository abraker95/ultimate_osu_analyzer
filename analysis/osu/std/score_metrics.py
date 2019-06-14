from enum import Enum
import numpy as np
import scipy.stats

from misc.numpy_utils import NumpyUtils
from misc.geometry import get_distance
from misc.math_utils import prob_not, prob_and, prob_or

from analysis.osu.std.score_data import StdScoreData


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
    def odds_all_players_tap_hitobject_within(per_hitobject_score_data, hitobject_idx, offset):
        return StdScoreData.odds_all_tap_within(per_hitobject_score_data[hitobject_idx], offset)


    @staticmethod
    def odds_all_players_cursor_hitobject_within(per_hitobject_score_data, hitobject_idx, offset):
        return StdScoreData.odds_all_cursor_within(per_hitobject_score_data[hitobject_idx], offset)

    
    @staticmethod 
    def odds_all_players_condition_hitobject_within(per_hitobject_score_data, hitobject_idx, tap_offset, cursor_offset):
        return StdScoreData.odds_all_conditions_within(per_hitobject_score_data[hitobject_idx], tap_offset, cursor_offset)


    @staticmethod
    def trans_odds_players_taps(per_hitobject_score_data, offset):
        times = per_hitobject_score_data[:,0,0]
        odds  = [ StdScoreMetrics.odds_all_players_tap_hitobject_within(per_hitobject_score_data, i, offset) for i in range(len(per_hitobject_score_data)) ]

        return times, np.asarray(odds)


    @staticmethod
    def trans_odds_players_aim(per_hitobject_score_data, offset):
        times = per_hitobject_score_data[:,0,0]
        odds  = [ StdScoreMetrics.odds_all_players_cursor_hitobject_within(per_hitobject_score_data, i, offset) for i in range(len(per_hitobject_score_data)) ]

        return times, np.asarray(odds)


    @staticmethod
    def trans_odds_players_condition(per_hitobject_score_data, tap_offset, cursor_offset):
        times = per_hitobject_score_data[:,0,0]
        odds  = [ StdScoreMetrics.odds_all_players_condition_hitobject_within(per_hitobject_score_data, i, tap_offset, cursor_offset) for i in range(len(per_hitobject_score_data)) ]

        return times, np.asarray(odds)