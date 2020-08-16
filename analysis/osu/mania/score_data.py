from enum import Enum
import numpy as np
import pandas as pd
import scipy.stats
import math

from analysis.osu.mania.action_data import ManiaActionData
from osu.local.hitobject.mania.mania import Mania

from misc.numpy_utils import NumpyUtils
from misc.math_utils import prob_trials


class ManiaScoreDataEnums(Enum):

    TIME          = 0
    COLUMN        = 1
    HIT_OFFSET    = 2
    HITOBJECT_IDX = 4


class ManiaScoreData():

    TYPE_HITP  = 0  # A hit press has a hitobject and offset associated with it
    TYPE_HITR  = 1  # A hit release has a hitobject and offset associated with it
    TYPE_MISS  = 2  # A miss has a hitobject associated with it, but not offset
    TYPE_EMPTY = 3  # An empty has neither hitobject nor offset associated with it

    DATA_OFFSET  = 0 
    DATA_TYPE    = 1
    DATA_MAP_IDX = 2

    pos_hit_range       = 100  # ms range of the late hit window
    neg_hit_range       = 100  # ms range of the early hit window
    pos_hit_miss_range  = 50   # ms range of the late miss window
    neg_hit_miss_range  = 50   # ms range of the early miss window

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
    lazy_sliders = True  # Release timings are currently not processed, TODO

    # There are cases for which parts of the hitwindow of multiple notes may overlap. If True, all 
    # overlapped miss parts are processed for one key event. If False, each overlapped miss part is 
    # processed for each individual key event.
    overlap_miss_handling = False

    # There are cases for which parts of the hitwindow of multiple notes may overlap. If True, all 
    # overlapped hit parts are processed for one key event. If False, each overlapped hit part is 
    # processed for each individual key event.
    overlap_hit_handling  = False

    @staticmethod
    def get_score_data(map_data, replay_data):
        """
        [
            [
                [ offset, type, action_idx ],
                [ offset, type, action_idx ],
                ... N events in col 
            ],
            [
                [ offset, type, action_idx ],
                [ offset, type, action_idx ],
                ... N events in col 
            ],
            ... N cols
        ]
        """
        pos_nothing_range = ManiaScoreData.pos_hit_range + ManiaScoreData.pos_hit_miss_range
        neg_nothing_range = ManiaScoreData.neg_hit_range + ManiaScoreData.neg_hit_miss_range

        score_data = []

        # Go through each column
        for map_col_idx, replay_col_idx in zip(map_data, replay_data):
            presses_map  = map_data[map_col_idx][map_data[map_col_idx] == ManiaActionData.PRESS]
            releases_map = map_data[map_col_idx][map_data[map_col_idx] == ManiaActionData.RELEASE]

            replay_col = replay_data[replay_col_idx]

            column_data = {}

            map_idx = 0
            replay_idx = 0

            # Go through each hitobject in column
            while True:
                # Condition checks whether we processed all notes in the column
                if map_idx >= len(presses_map): break

                # Get note timings
                note_start_time = presses_map.index[map_idx]
                note_end_time   = releases_map.index[map_idx]
                
                # Single notes have different behavior than long notes
                is_single_note = ((note_end_time - note_start_time) <= 1)

                # To keep track of whether there was a tap that corresponded to this hitobject
                is_note_consumed = False

                # Modify hit windows
                if ManiaScoreData.notelock:
                    # TODO:
                    # neg 
                    # neg_miss_range = 
                    pass

                if ManiaScoreData.dynamic_window:
                    # TODO
                    pass
                
                '''
                if len(replay_data[col]) == 0: replay_idx = 0
                else:
                    # Get first replay event that leaves the hitobject's positive miss window
                    lookforward_time = note_start_time + ManiaScoreData.pos_hit_range + ManiaScoreData.pos_hit_miss_range
                    replay_idx = replay_data[col][replay_data[col].index >= lookforward_time]

                    # If there are no replay events after the hitobject, get up to the last one;
                    # if curr_key_event_idx is equal to it, then the for loop isn't going to run anyway
                    if len(key_event_idx) == 0: key_event_idx = len(event_data)
                    else:                       key_event_idx = key_event_idx[0]
                '''
                
                # Go through replay events
                while True:
                    # Condition check whether all player actions in the column have been processed
                    # It's possible that the player never pressed any keys, so this may hit more
                    # often than one may expect
                    if replay_idx >= len(replay_col): break

                    # Advance map_idx before continuing going through replay_idx
                    if is_note_consumed: break

                    # Time at which press or release occurs
                    replay_timing = replay_col.index[replay_idx]

                    # If a press occurs at this time
                    if replay_col.iloc[replay_idx] == ManiaActionData.PRESS:
                        time_offset = replay_timing - note_start_time

                        # Way early taps. Miss if blank miss is on -> record miss, otherwise ignore
                        is_in_neg_nothing_range = time_offset < -neg_nothing_range
                        if is_in_neg_nothing_range:
                            if ManiaScoreData.blank_miss:
                                column_data[replay_timing] = np.asarray([ np.nan, ManiaScoreData.TYPE_EMPTY, None ])
                            
                            replay_idx += 1
                            continue

                        # Way late taps. Doesn't matter where, ignore these
                        is_in_pos_nothing_range = time_offset > pos_nothing_range
                        if is_in_pos_nothing_range:
                            if ManiaScoreData.blank_miss:
                                column_data[replay_timing] = np.asarray([ np.nan, ManiaScoreData.TYPE_EMPTY, None ])

                            replay_idx += 1
                            continue

                        # Early miss tap
                        is_in_neg_miss_range = time_offset < -ManiaScoreData.neg_hit_range
                        if is_in_neg_miss_range:
                            column_data[replay_timing] = np.asarray([ -float(neg_nothing_range), ManiaScoreData.TYPE_MISS, map_idx ])
                            
                            # Consume if release timing processing isn't needed
                            if is_single_note or ManiaScoreData.lazy_sliders:
                                is_note_consumed = True

                            replay_idx += 1
                            continue

                        # Late miss tap
                        is_in_pos_miss_range = time_offset > ManiaScoreData.pos_hit_range
                        if is_in_pos_miss_range:
                            column_data[replay_timing] = np.asarray([ float(pos_nothing_range), ManiaScoreData.TYPE_MISS, map_idx ])
                            
                            # Consume if release timing processing isn't needed
                            if is_single_note or ManiaScoreData.lazy_sliders:
                                is_note_consumed = True

                            replay_idx += 1
                            continue

                        # If none of the above, then it's a hit
                        column_data[replay_timing] = np.asarray([ time_offset, ManiaScoreData.TYPE_HITP, map_idx ])

                        # Consume if release timing processing isn't needed
                        if is_single_note or ManiaScoreData.lazy_sliders:
                            is_note_consumed = True

                        replay_idx += 1
                        continue

                    # If a release occurs at this time
                    if replay_col.iloc[replay_idx] == ManiaActionData.RELEASE:
                        # If this is true, then release timings are ignored
                        if ManiaScoreData.lazy_sliders:
                            # This assumes there is a press associated with this release
                            #is_note_consumed = True

                            replay_idx += 1
                            continue

                        time_offset = replay_timing - note_end_time

                        # TODO: Handle release

                        # If none of the above, then it's a hit
                        column_data[replay_timing] = np.asarray([ time_offset, ManiaScoreData.TYPE_HITR, map_idx ])

                        # This assumes there is a press associated with this release
                        #is_note_consumed = True

                        replay_idx += 1
                        continue                        

                    # If we are here then it's a HOLD or RELEASE. Ignore.
                    replay_idx += 1
                    continue

                if not is_note_consumed:
                    process_as_release = not is_single_note and not ManiaScoreData.lazy_sliders
                    replay_timing = replay_col.index[replay_idx]

                    if process_as_release:
                        time_offset = replay_timing - note_end_time
                        note_timing = note_end_time
                    else:
                        time_offset = replay_timing - note_start_time
                        note_timing = note_start_time

                    # If the note is not consumed, check if replay timing has passed it
                    # If it did, then it's a miss. Otherwise don't consume it yet
                    if time_offset > pos_nothing_range:
                        column_data[note_timing] = np.asarray([ float(pos_nothing_range), ManiaScoreData.TYPE_MISS, map_idx ])
                        map_idx += 1
                # Note was consumed
                else:
                    map_idx += 1
                    is_note_consumed = False

            # Sort data by timings
            column_data = dict(sorted(column_data.items()))

            # Convert the dictionary of recorded timings and states into a pandas data
            column_data = pd.DataFrame.from_dict(column_data, orient='index')
            score_data.append(column_data)

        # This turns out to be 3 dimensional data (indexed by columns, timings, and attributes)
        return pd.concat(score_data, axis=0, keys=range(len(map_data)))


    @staticmethod
    def filter_by_hit_type(score_data, hit_types, invert=False):
        if type(hit_types) != list: hit_types = [ hit_types ]
        
        mask = score_data[ManiaScoreData.DATA_TYPE] == hit_types[0]
        if len(hit_types) > 1:
            for hit_type in hit_types[1:]:
                mask |= score_data[ManiaScoreData.DATA_TYPE] == hit_type

        return score_data[~mask] if invert else score_data[mask]


    @staticmethod
    def press_interval_mean(score_data):
        # TODO need to put in release offset into score_data
        # TODO need to go through hitobjects and filter out hold notes
        #  
        pass


    @staticmethod
    def tap_offset_mean(score_data):
        score_data = ManiaScoreData.filter_by_hit_type(score_data, [ManiaScoreData.TYPE_EMPTY], invert=True)
        score_data = score_data[ManiaScoreData.DATA_OFFSET]
        return np.mean(score_data)


    @staticmethod
    def tap_offset_var(score_data):
        score_data = ManiaScoreData.filter_by_hit_type(score_data, [ManiaScoreData.TYPE_EMPTY], invert=True)
        score_data = score_data[ManiaScoreData.DATA_OFFSET]
        return np.var(score_data)


    @staticmethod
    def tap_offset_stdev(score_data):
        score_data = ManiaScoreData.filter_by_hit_type(score_data, [ManiaScoreData.TYPE_EMPTY], invert=True)
        score_data = score_data[ManiaScoreData.DATA_OFFSET]
        return np.std(score_data)


    @staticmethod
    def model_offset_prob(mean, stdev, offset):
        prob_less_than_neg = scipy.stats.norm.cdf(-offset, loc=mean, scale=stdev)
        prob_less_than_pos = scipy.stats.norm.cdf(offset, loc=mean, scale=stdev)

        return prob_less_than_pos - prob_less_than_neg


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

        return ManiaScoreData.model_offset_prob(mean, stdev, offset)


    @staticmethod
    def odds_all_tap_within(score_data, offset):    
        """
        Creates a gaussian distribution model using avg and var of tap offsets and calculates the odds that all hits
        are within the specified offset

        Returns: probability all random values [X] are between -offset <= X <= offset
                TL;DR: look at all the hits for scores; What are the odds all of them are between -offset and offset?
        """
        score_data = ManiaScoreData.filter_by_hit_type(score_data, [ManiaScoreData.TYPE_EMPTY], invert=True)
        num_taps = len(score_data[ManiaScoreData.DATA_OFFSET])

        return ManiaScoreData.odds_some_tap_within(score_data, offset)**num_taps

    
    @staticmethod
    def odds_all_tap_within_trials(score_data, offset, trials):
        """
        Creates a gaussian distribution model using avg and var of tap offsets and calculates the odds that all hits
        are within the specified offset after the specified number of trials

        Returns: probability all random values [X] are between -offset <= X <= offset after trial N
                TL;DR: look at all the hits for scores; What are the odds all of them are between -offset and offset during any of the number
                        of attempts specified?
        """
        return prob_trials(ManiaScoreData.odds_all_tap_within(score_data, offset), trials)


    @staticmethod
    def model_ideal_acc(mean, stdev, num_notes, score_point_judgements=None):
        """
        Set for OD8
        """
        prob_less_than_max  = ManiaScoreData.model_offset_prob(mean, stdev, 16.5)
        prob_less_than_300  = ManiaScoreData.model_offset_prob(mean, stdev, 40.5)
        prob_less_than_200  = ManiaScoreData.model_offset_prob(mean, stdev, 73.5)
        prob_less_than_100  = ManiaScoreData.model_offset_prob(mean, stdev, 103.5)
        prob_less_than_50   = ManiaScoreData.model_offset_prob(mean, stdev, 127.5)

        prob_max  = prob_less_than_max
        prob_300  = prob_less_than_300 - prob_max
        prob_200  = prob_less_than_200 - prob_less_than_300
        prob_100  = prob_less_than_100 - prob_less_than_200
        prob_50   = prob_less_than_50 - prob_less_than_100
        prob_miss = 1 - prob_less_than_50

        total_points_of_hits = (prob_50*50 + prob_100*100 + prob_200*200 + prob_300*300 + prob_max*300)*(num_notes - num_notes*prob_miss)

        return total_points_of_hits / (num_notes * 300)


    @staticmethod
    def model_ideal_acc_data(score_data, score_point_judgements=None):
        """
        Set for OD8
        """
        mean      = ManiaScoreData.tap_offset_mean(score_data)
        stdev     = ManiaScoreData.tap_offset_stdev(score_data)
        num_taps  = len(score_data[ManiaScoreData.DATA_OFFSET])

        return ManiaScoreData.model_ideal_acc(mean, stdev, num_taps, score_point_judgements)


    @staticmethod
    def model_num_hits(mean, stdev, num_notes):
        # Calculate probabilities of hits being within offset of the resultant gaussian distribution
        prob_less_than_max  = ManiaScoreData.model_offset_prob(mean, stdev, 16.5)
        prob_less_than_300  = ManiaScoreData.model_offset_prob(mean, stdev, 40.5)
        prob_less_than_200  = ManiaScoreData.model_offset_prob(mean, stdev, 73.5)
        prob_less_than_100  = ManiaScoreData.model_offset_prob(mean, stdev, 103.5)
        prob_less_than_50   = ManiaScoreData.model_offset_prob(mean, stdev, 127.5)

        prob_max  = prob_less_than_max
        prob_300  = prob_less_than_300 - prob_max
        prob_200  = prob_less_than_200 - prob_less_than_300
        prob_100  = prob_less_than_100 - prob_less_than_200
        prob_50   = prob_less_than_50 - prob_less_than_100
        prob_miss = 1 - prob_less_than_50

        # Get num of hitobjects that ideally would occur based on the gaussian distribution
        num_max  = prob_max*num_notes
        num_300  = prob_300*num_notes
        num_200  = prob_200*num_notes
        num_100  = prob_100*num_notes
        num_50   = prob_50*num_notes
        num_miss = prob_miss*num_notes

        return num_max, num_300, num_200, num_100, num_50, num_miss


    @staticmethod
    def odds_acc(score_data, target_acc):
        num_notes = len(np.vstack(score_data))
        mean      = ManiaScoreData.tap_offset_mean(score_data)

        def get_stdev_from_acc(acc):
            stdev    = ManiaScoreData.tap_offset_stdev(score_data)
            curr_acc = ManiaScoreData.model_ideal_acc_data(score_data)

            cost = round(acc, 3) - round(curr_acc, 3)
            rate = 1

            while cost != 0:
                stdev -= cost*rate

                curr_acc = ManiaScoreData.model_ideal_acc(mean, stdev, num_notes)
                cost = round(acc, 3) - round(curr_acc, 3)

            return stdev

        # Fit a normal distribution to the desired acc
        stdev = get_stdev_from_acc(target_acc)

        # Get the number of resultant hits from that distribution
        num_max, num_300, num_200, num_100, num_50, num_miss = ManiaScoreData.model_num_hits(mean, stdev, num_notes)

        # Get the stdev of of the replay data
        stdev = ManiaScoreData.tap_offset_stdev(score_data)

        # Get probabilites the number of score points are within hit window based on replay
        prob_less_than_max = scipy.stats.binom.sf(num_max - 1, num_notes, ManiaScoreData.model_offset_prob(mean, stdev, 16.5))
        prob_less_than_300 = scipy.stats.binom.sf(num_max + num_300 - 1, num_notes, ManiaScoreData.model_offset_prob(mean, stdev, 40.5))
        prob_less_than_200 = scipy.stats.binom.sf(num_max + num_300 + num_200 - 1, num_notes, ManiaScoreData.model_offset_prob(mean, stdev, 73.5))
        prob_less_than_100 = scipy.stats.binom.sf(num_max + num_300 + num_200 + num_100 - 1, num_notes, ManiaScoreData.model_offset_prob(mean, stdev, 103.5))
        prob_less_than_50  = scipy.stats.binom.sf(num_max + num_300 + num_200 + num_100 + num_50 - 1, num_notes, ManiaScoreData.model_offset_prob(mean, stdev, 127.5))

        return prob_less_than_max*prob_less_than_300*prob_less_than_200*prob_less_than_100*prob_less_than_50