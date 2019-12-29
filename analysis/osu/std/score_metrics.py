from enum import Enum
import numpy as np
import scipy.stats

from misc.numpy_utils import NumpyUtils
from misc.geometry import get_distance
from misc.math_utils import prob_not, prob_and, prob_or

from analysis.osu.std.score_data import StdScoreData, StdScoreDataEnums


class StdScoreMetrics():
    """
    Class used for analyzing mass score data and player statistics.
    """

    @staticmethod
    def get_per_hitobject_score_data(score_data_array):
        """
        Takes arrays of score data pertaining to various players and transposes it to be an array of per-hitobject score data
        by various players. In other words, it stacks all score data per-notes instead of standalone per-player. It allows to
        easier calculate data based how players do on specific notes or pattens. If ``a0`` corresponds to player a and note 0, 
        then the data
        ::
            [
                [
            a0      [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
            a1      [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
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
        ::
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

        Parameters
        ----------
        score_data_array : numpy.array
            List of ``score_data`` numpy arrays

        Returns
        -------
        numpy.array
        """
        return np.transpose(score_data_array, axes=(1, 0, 2))


    @staticmethod
    def get_percent_below_offset_one(per_hitobject_score_data, hitobject_idx, offset):
        """
        Gives the % of players that tapped within ``offset`` for the hitobject at ``hitobject_idx``.

        Parameters
        ----------
        per_hitobject_score_data : numpy.array
            Per-hitobject score data across various plays

        hitobject_idx : int
            The index of the note to solve for

        offset : float
            Offset serves as a threshold for the percent calculation

        Returns
        -------
        float
            % of players able to hit better than ``offset`` based on given 
            mass score data in ``per_hitobject_score_data``.
        """
        hit_offsets = per_hitobject_score_data[hitobject_idx][:, StdScoreDataEnums.HIT_OFFSET.value]
        hit_offsets_below_offset = hit_offsets[abs(hit_offsets) < offset]

        return len(hit_offsets_below_offset)/len(hit_offsets)


    @staticmethod
    def percent_players_taps_all(per_hitobject_score_data, offset):
        """
        Gives the % of players that tapped within ``offset`` for each hitobject.

        Parameters
        ----------
        per_hitobject_score_data : numpy.array
            Per-hitobject score data across various plays

        offset : float
            Offset serves as a threshold for the percent calculation

        Returns
        -------
        (float, numpy.array)
            A tuple ``(times, percents)``. Percents correspond to how much % of players tapped
            within ``offset`` for a list of hitobject. Times correspond to the timing of the
            respective hitobjects.
        """
        times   = per_hitobject_score_data[:,0,0]
        percent = [ StdScoreMetrics.get_percent_below_offset_one(per_hitobject_score_data, i, offset) for i in range(len(per_hitobject_score_data)) ]

        return times, np.asarray(percent)


    @staticmethod
    def solve_for_hit_offset_one(per_hitobject_score_data, hitobject_idx, target_percent):
        """
        Solves for the tapping offset for a given note such that a certain percentage, 
        ``target_percent``, of players are able to hit better than.

        Parameters
        ----------
        per_hitobject_score_data : numpy.array
            Per-hitobject score data across various plays

        hitobject_idx : int
            The index of the note to solve for

        target_percent : float
            Target percentage of players

        Returns
        -------
        float
            The tap offset from 0ms that would satisfy ``target_percent`` % of players being able to hit better than.
        """
        offset         = 0
        target_percent = min(max(0.0, target_percent), 1.0)
        curr_percent   = StdScoreMetrics.get_percent_below_offset_one(per_hitobject_score_data, hitobject_idx, offset)

        while curr_percent < target_percent:
            curr_percent = StdScoreMetrics.get_percent_below_offset_one(per_hitobject_score_data, hitobject_idx, offset)
            offset += 1

        return offset


    @staticmethod
    def solve_for_hit_offset_all(per_hitobject_score_data):
        """
        Takes all of the players' results to solve for the tapping offset 50% of players are able to 
        hit better than for each note. This is useful for determining the difficulty response of 
        patterns in the map relative to other patterns in the same map.

        Parameters
        ----------
        per_hitobject_score_data : numpy.array
            Per-hitobject score data across various plays

        Returns
        -------
        (float, numpy.array)
            A tuple ``(times, offsets)``. Offsets correspond to each hitobject where 50% of 
            players are able to hit better than. Times correspond to the timing of the
            respective hitobjects.
        """
        times       = per_hitobject_score_data[:,0,0]
        hit_offsets = [ StdScoreMetrics.solve_for_hit_offset_one(per_hitobject_score_data, i, 0.5) for i in range(len(per_hitobject_score_data)) ]

        return times, np.asarray(hit_offsets)