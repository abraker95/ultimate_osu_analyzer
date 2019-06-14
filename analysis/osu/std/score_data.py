from enum import Enum
import numpy as np
import scipy.stats

from misc.numpy_utils import NumpyUtils
from misc.geometry import get_distance
from misc.math_utils import prob_not, prob_and, prob_or

from osu.local.hitobject.std.std import Std
from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.replay_data import StdReplayData


class StdScoreDataEnums(Enum):

    TIME          = 0
    POS           = 1
    HIT_OFFSET    = 2
    POS_OFFSET    = 3
    HITOBJECT_IDX = 4


'''
[
    [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
    ...  N events
]
'''
class StdScoreData():

    pos_hit_range      = 100   # ms range of the late hit window
    neg_hit_range      = 100   # ms range of the early hit window
    pos_hit_miss_range = 50    # ms range of the late miss window
    neg_hit_miss_range = 50    # ms range of the early miss window

    dist_miss_range = 50       # ms range the cursor can deviate from aimpoint distance threshold before it's a miss

    pos_rel_range       = 100  # ms range of the late release window
    neg_rel_range       = 100  # ms range of the early release window
    pos_rel_miss_range  = 50   # ms range of the late release window
    neg_rel_miss_range  = 50   # ms range of the early release window

    hitobject_radius = Std.cs_to_px(4)  # Radius from hitobject for which cursor needs to be within for a tap to count
    follow_radius    = Std.cs_to_px(4)  # Radius from slider aimpoint for which cursor needs to be within for a hold to count

    # Disables hitting next note too early. If False, the neg_miss_range of the current note is 
    # overridden to extend to the previous note's pos_hit_range boundary.
    notelock = True

    # Overrides the miss and hit windows to correspond to spacing between notes. If True then all 
    # the ranges are are overridden to be split up in 1/4th sections relative to the distance between 
    # current and next notes
    dynamic_window = False

    # Enables missing in blank space. If True, the Nothing window behaves like the miss window, but the 
    # iterator does not go to the next note.
    blank_miss = False

    # If True, remove release miss window for sliders. This allows to hit sliders and release them whenever
    lazy_sliders = False

    # There are cases for which parts of the hitwindow of multiple notes may overlap. If True, all 
    # overlapped miss parts are processed for one key event. If False, each overlapped miss part is 
    # processed for each individual key event.
    overlap_miss_handling = False

    # There are cases for which parts of the hitwindow of multiple notes may overlap. If True, all 
    # overlapped hit parts are processed for one key event. If False, each overlapped hit part is 
    # processed for each individual key event.
    overlap_hit_handling  = False

    @staticmethod
    def get_score_data(replay_data, map_data):
        pos_nothing_range = StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range
        neg_nothing_range = StdScoreData.neg_hit_range + StdScoreData.neg_hit_miss_range

        event_data = StdReplayData.press_start_end_times(replay_data)
        curr_key_event_idx = 0
        score_data = []

        # Go through each hitobject
        for hitobject_idx in range(len(map_data)):
            # Get first aimpoint in the hitobject
            aimpoint_time, aimpoint_cor = map_data[hitobject_idx][0]

            # To keep track of whether there was a tap that corresponded to this hitobject
            is_hitobject_consumed = False

            # Modify hit windows
            if StdScoreData.notelock:
                # TODO:
                prev_aimpoint_time, prev_aimpoint_cor = map_data[hitobject_idx - 1][0]
                # neg 
                # neg_miss_range = 
                pass

            if StdScoreData.dynamic_window:
                # TODO
                pass

            if len(event_data) == 0: key_event_idx = 0
            else:
                # Get first replay event that leaeves the hitobject's positive miss window
                lookforward_time = aimpoint_time + StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range
                key_event_idx = np.where(event_data[:,1] >= lookforward_time)[0]

                # If there are no replay events after the hitobject, get up to the last one;
                # if curr_key_event_idx is equal to it, then the for loop isn't going to run anyway
                if len(key_event_idx) == 0: key_event_idx = len(event_data)
                else:                       key_event_idx = key_event_idx[0]
            
            # Go through unprocessed replay events
            for idx in range(curr_key_event_idx, key_event_idx):
                press_idx, press_time, release_idx, release_time = event_data[idx]
                time_offset = press_time - aimpoint_time

                cursor_cor = np.asarray([ replay_data[int(press_idx)][1], replay_data[int(press_idx)][2] ])
                pos_offset = get_distance(cursor_cor, aimpoint_cor)

                #score_data.append([ press_time, cursor_cor, offset, key_event_idx, len(event_data) ])
                
                # Way early taps. Doesn't matter where, is a miss if blank miss is on, otherwise ignore these
                is_in_neg_nothing_range = time_offset < -neg_nothing_range
                if is_in_neg_nothing_range:
                    if StdScoreData.blank_miss:
                        score_data.append([ press_time, cursor_cor, float('nan'), (float('nan'), float('nan')), float('nan') ])
                    curr_key_event_idx = idx + 1  # consume event
                    continue                      # next key press

                # Way late taps. Doesn't matter where, ignore these
                is_in_pos_nothing_range = time_offset > pos_nothing_range
                if is_in_pos_nothing_range:
                    if StdScoreData.blank_miss:
                        score_data.append([ press_time, cursor_cor, float('nan'), (float('nan'), float('nan')), float('nan') ])
                    curr_key_event_idx = idx + 1  # consume event
                    continue                      # next key press

                # Early miss tap if on circle
                is_in_neg_miss_range = time_offset < -StdScoreData.neg_hit_range
                if is_in_neg_miss_range:
                    if pos_offset < StdScoreData.hitobject_radius:
                        score_data.append([ press_time, cursor_cor, float('-inf'), (float('nan'), float('nan')), hitobject_idx ])
                        curr_key_event_idx    = idx + 1      # consume event
                        is_hitobject_consumed = True; break  # consume hitobject

                # Late miss tap if on circle
                is_in_pos_miss_range = time_offset > StdScoreData.pos_hit_range
                if is_in_pos_miss_range:
                    if pos_offset < StdScoreData.hitobject_radius:
                        score_data.append([ press_time, cursor_cor, float('inf'), (float('nan'), float('nan')), hitobject_idx ])
                        curr_key_event_idx    = idx + 1      # consume event
                        is_hitobject_consumed = True; break  # consume hitobject

                # If a tap is anything else, it's a hit if on circle
                if pos_offset < StdScoreData.hitobject_radius:
                    score_data.append([ press_time, cursor_cor, time_offset, cursor_cor - aimpoint_cor, hitobject_idx ])

                    if not StdScoreData.lazy_sliders:
                        # TODO: Handle sliders here
                        # TODO: compare release_time against slider release window
                        pass

                    curr_key_event_idx    = idx + 1      # consume event
                    is_hitobject_consumed = True; break  # consume hitobject

                # If we are here, then the tap would be a hit if it were to be on a circle
                # In such case, the hit is ignored
                curr_key_event_idx = idx + 1  # consume event

            # If the hitobject is not consumed after all that, it's a miss.
            # The player never tapped this hitobject. 
            if not is_hitobject_consumed:
                idx = min(curr_key_event_idx, len(event_data) - 1)
                score_data.append([ aimpoint_time, aimpoint_cor, float(StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range), (float('nan'), float('nan')), hitobject_idx ])

        return np.asarray(score_data)


    @staticmethod
    def tap_offset_mean(score_data):
        return np.mean(score_data[:, StdScoreDataEnums.HIT_OFFSET.value])


    @staticmethod
    def tap_offset_var(score_data):
        return np.var(score_data[:, StdScoreDataEnums.HIT_OFFSET.value])


    @staticmethod
    def tap_offset_stdev(score_data):
        return np.std(score_data[:, StdScoreDataEnums.HIT_OFFSET.value])


    @staticmethod
    def cursor_pos_offset_mean(score_data):
        mean_x = np.mean(score_data[:, StdScoreDataEnums.POS_OFFSET.value][0])
        mean_y = np.mean(score_data[:, StdScoreDataEnums.POS_OFFSET.value][1])
        return (mean_x, mean_y)


    @staticmethod
    def cursor_pos_offset_var(score_data):
        var_x = np.var(score_data[:, StdScoreDataEnums.POS_OFFSET.value][0])
        var_y = np.var(score_data[:, StdScoreDataEnums.POS_OFFSET.value][1])

        return (var_x, var_y)


    @staticmethod
    def cursor_pos_offset_stdev(score_data):
        stdev_x = np.std(score_data[:, StdScoreDataEnums.POS_OFFSET.value][0])
        stdev_y = np.std(score_data[:, StdScoreDataEnums.POS_OFFSET.value][1])

        return (stdev_x, stdev_y)


    @staticmethod
    def odds_all_tap_within(score_data, offset):
        """
        Creates a gaussian distribution using avg and var of tap offsets and calculates the odds that all of the hits 
        are within the specified offset

        Returns: probability one random value [X] is between -offset <= X <= offset
                 To calculate the odds of all taps occuring within offset, do odds_all_tap_within(score_data, offset)**len(score_data)
        """
        mean  = StdScoreData.tap_offset_mean(score_data)
        stdev = StdScoreData.tap_offset_stdev(score_data)

        prob_less_than_neg = scipy.stats.norm.cdf(-offset, loc=mean, scale=stdev)
        prob_less_than_pos = scipy.stats.norm.cdf(offset, loc=mean, scale=stdev)

        return prob_less_than_pos - prob_less_than_neg


    @staticmethod
    def odds_all_cursor_within(score_data, offset):
        """
        Creates a gaussian distribution using avg and var of cursor 2D position offsets and uses it to calculates the odds 
        that all of the cursor positions are within the specified distance from the center of all hitobjects

        Returns: probability one random value [X, Y] is between (-offset, -offset) <= (X, Y) <= (offset, offset)
                 To calculate the odds of all cursor positions occuring within offset, do odds_all_cursor_within(score_data, offset)**len(score_data)
        """
        positions = np.stack(score_data[:, StdScoreDataEnums.POS_OFFSET.value], axis=0)

        mean_2d      = np.asarray(StdScoreData.cursor_pos_offset_mean(score_data))
        covariance   = np.cov(positions.T)
        distribution = scipy.stats.multivariate_normal(mean_2d, covariance)

        prob_less_than_neg = distribution.cdf(np.asarray([-offset, -offset]))
        prob_less_than_pos = distribution.cdf(np.asarray([offset, offset]))

        return prob_less_than_pos - prob_less_than_neg