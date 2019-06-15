from enum import Enum
import numpy as np
import scipy.stats

from osu.local.hitobject.mania.mania import Mania
from analysis.osu.mania.replay_data import ManiaReplayData
from misc.numpy_utils import NumpyUtils



class ManiaScoreDataEnums(Enum):

    TIME          = 0
    COLUMN        = 1
    HIT_OFFSET    = 2
    HITOBJECT_IDX = 4


'''
[
    [
        [ press_time, column, offset, hitobject_idx ],
        [ press_time, column, offset, hitobject_idx ],
        ... N events in col 
    ],
    [
        [ press_time, column, offset, hitobject_idx ],
        [ press_time, column, offset, hitobject_idx ],
        ... N events in col 
    ],
    ... N cols
]
'''
class ManiaScoreData():

    pos_hit_range      = 100   # ms range of the late hit window
    neg_hit_range      = 100   # ms range of the early hit window
    pos_hit_miss_range = 50    # ms range of the late miss window
    neg_hit_miss_range = 50    # ms range of the early miss window

    dist_miss_range = 50       # ms range the cursor can deviate from aimpoint distance threshold before it's a miss

    pos_rel_range       = 100  # ms range of the late release window
    neg_rel_range       = 100  # ms range of the early release window
    pos_rel_miss_range  = 50   # ms range of the late release window
    neg_rel_miss_range  = 50   # ms range of the early release window

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
        pos_nothing_range = ManiaScoreData.pos_hit_range + ManiaScoreData.pos_hit_miss_range
        neg_nothing_range = ManiaScoreData.neg_hit_range + ManiaScoreData.neg_hit_miss_range

        score_data = []

        # Go through each column
        for column in range(len(map_data)):
            event_data  = ManiaReplayData.start_end_times(replay_data, column)
            curr_key_event_idx = 0
            column_data = []

            # Go through each hitobject in column
            for hitobject_idx in range(len(map_data[column])):
                # Get note timings
                note_start_time = map_data[column][hitobject_idx][0]
                note_end_time   = map_data[column][hitobject_idx][-1]

                # To keep track of whether there was a tap that corresponded to this hitobject
                is_hitobject_consumed = False

                # Modify hit windows
                if ManiaScoreData.notelock:
                    # TODO:
                    # neg 
                    # neg_miss_range = 
                    pass

                if ManiaScoreData.dynamic_window:
                    # TODO
                    pass

                if len(event_data) == 0: key_event_idx = 0
                else:
                    # Get first replay event that leaeves the hitobject's positive miss window
                    lookforward_time = note_start_time + ManiaScoreData.pos_hit_range + ManiaScoreData.pos_hit_miss_range
                    key_event_idx = np.where(event_data[:,0] >= lookforward_time)[0]

                    # If there are no replay events after the hitobject, get up to the last one;
                    # if curr_key_event_idx is equal to it, then the for loop isn't going to run anyway
                    if len(key_event_idx) == 0: key_event_idx = len(event_data)
                    else:                       key_event_idx = key_event_idx[0]
                
                # Go through unprocessed replay events
                for idx in range(curr_key_event_idx, key_event_idx):
                    press_time, release_time = event_data[idx]
                    time_offset = press_time - note_start_time

                    #column_data.append([ press_time, column, time_offset, hitobject_idx, idx ])
                    
                    # Way early taps. Doesn't matter where, is a miss if blank miss is on, otherwise ignore these
                    is_in_neg_nothing_range = time_offset < -neg_nothing_range
                    if is_in_neg_nothing_range:
                        if ManiaScoreData.blank_miss:
                            column_data.append([ press_time, column, np.nan, np.nan ])
                        curr_key_event_idx = idx + 1  # consume event
                        continue                      # next key press

                    # Way late taps. Doesn't matter where, ignore these
                    is_in_pos_nothing_range = time_offset > pos_nothing_range
                    if is_in_pos_nothing_range:
                        if ManiaScoreData.blank_miss:
                            column_data.append([ press_time, column, np.nan, np.nan ])
                        curr_key_event_idx = idx + 1  # consume event
                        continue                      # next key press

                    # Early miss tap if on circle
                    is_in_neg_miss_range = time_offset < -ManiaScoreData.neg_hit_range
                    if is_in_neg_miss_range:
                        column_data.append([ press_time, column, -float(ManiaScoreData.pos_hit_range + ManiaScoreData.pos_hit_miss_range), hitobject_idx ])
                        curr_key_event_idx    = idx + 1      # consume event
                        is_hitobject_consumed = True; break  # consume hitobject

                    # Late miss tap if on circle
                    is_in_pos_miss_range = time_offset > ManiaScoreData.pos_hit_range
                    if is_in_pos_miss_range:
                        column_data.append([ press_time, column, float(ManiaScoreData.pos_hit_range + ManiaScoreData.pos_hit_miss_range), hitobject_idx ])
                        curr_key_event_idx    = idx + 1      # consume event
                        is_hitobject_consumed = True; break  # consume hitobject

                    # If a tap is anything else, it's a hit
                    column_data.append([ press_time, column, time_offset, hitobject_idx ])

                    if not ManiaScoreData.lazy_sliders:
                        # TODO: Handle sliders here
                        # TODO: compare release_time against slider release window
                        pass

                    curr_key_event_idx    = idx + 1      # consume event
                    is_hitobject_consumed = True; break  # consume hitobject

                # If the hitobject is not consumed after all that, it's a miss.
                # The player never tapped this hitobject. 
                if not is_hitobject_consumed:
                    idx = min(curr_key_event_idx, len(event_data) - 1)
                    column_data.append([ note_start_time, column, float(ManiaScoreData.pos_hit_range + ManiaScoreData.pos_hit_miss_range), hitobject_idx ])

            score_data.append(np.asarray(column_data))

        return np.asarray(score_data)


    @staticmethod
    def press_interval_mean(score_data):
        # TODO need to put in release offset into score_data
        # TODO need to go through hitobjects and filter out hold notes
        #  
        pass


    @staticmethod
    def tap_offset_mean(score_data):
        hit_offsets = np.vstack(score_data)[:, ManiaScoreDataEnums.HIT_OFFSET.value]
        
        hit_offsets[hit_offsets == float('inf')]  = ManiaScoreData.pos_hit_range + ManiaScoreData.pos_hit_miss_range
        hit_offsets[hit_offsets == float('-inf')] = -(ManiaScoreData.neg_hit_range + ManiaScoreData.neg_hit_miss_range)
        hit_offsets = hit_offsets[~np.isnan(hit_offsets.astype(float))]

        return np.mean(hit_offsets)


    @staticmethod
    def tap_offset_var(score_data):
        hit_offsets = np.vstack(score_data)[:, ManiaScoreDataEnums.HIT_OFFSET.value]
        
        hit_offsets[hit_offsets == float('inf')]  = ManiaScoreData.pos_hit_range + ManiaScoreData.pos_hit_miss_range
        hit_offsets[hit_offsets == float('-inf')] = -(ManiaScoreData.neg_hit_range + ManiaScoreData.neg_hit_miss_range)
        hit_offsets = hit_offsets[~np.isnan(hit_offsets.astype(float))]

        return np.var(hit_offsets)


    @staticmethod
    def tap_offset_stdev(score_data):
        hit_offsets = np.vstack(score_data)[:, ManiaScoreDataEnums.HIT_OFFSET.value]
        
        hit_offsets[hit_offsets == float('inf')]  = ManiaScoreData.pos_hit_range + ManiaScoreData.pos_hit_miss_range
        hit_offsets[hit_offsets == float('-inf')] = -(ManiaScoreData.neg_hit_range + ManiaScoreData.neg_hit_miss_range)
        hit_offsets = hit_offsets[~np.isnan(hit_offsets.astype(float))]

        return np.std(hit_offsets)


    @staticmethod
    def odds_some_tap_within(score_data, offset):
        """
        Creates a gaussian distribution model using avg and var of tap offsets and calculates the odds that some hit
        is within the specified offset

        Returns: probability one random value [X] is between -offset <= X <= offset
                 TL;DR: look at all the hits for scores; What are the odds of you picking 
                        a random hit that is between -offset and offset?
        """
        mean  = ManiaScoreData.tap_offset_mean(score_data)
        stdev = ManiaScoreData.tap_offset_stdev(score_data)

        prob_less_than_neg = scipy.stats.norm.cdf(-offset, loc=mean, scale=stdev)
        prob_less_than_pos = scipy.stats.norm.cdf(offset, loc=mean, scale=stdev)

        return prob_less_than_pos - prob_less_than_neg


    """
    Creates a gaussian distribution model using avg and var of tap offsets and calculates the odds that all hits
    are within the specified offset

    Returns: probability all random values [X] are between -offset <= X <= offset
             TL;DR: look at all the hits for scores; What are the odds all of them are between -offset and offset?
    """
    @staticmethod
    def odds_all_tap_within(score_data, offset):
        return ManiaScoreData.odds_some_tap_within(score_data, offset)**len(np.vstack(score_data))

    
    """
    Creates a gaussian distribution model using avg and var of tap offsets and calculates the odds that all hits
    are within the specified offset after the specified number of trials

    Returns: probability all random values [X] are between -offset <= X <= offset after trial N
             TL;DR: look at all the hits for scores; What are the odds all of them are between -offset and offset during any of the number
                    of attempts specified?
    """
    @staticmethod
    def odds_all_tap_within_trials(score_data, offset, trials):
        return prob_trials(ManiaScoreData.odds_all_tap_within(score_data, offset), trials)