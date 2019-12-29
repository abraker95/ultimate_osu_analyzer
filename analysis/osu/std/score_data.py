from enum import Enum
import numpy as np
import scipy.stats

from misc.numpy_utils import NumpyUtils
from misc.geometry import get_distance
from misc.math_utils import prob_not, prob_and, prob_or

from osu.local.hitobject.std.std import Std
from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.replay_data import StdReplayData
from analysis.osu.std.replay_metrics import StdReplayMetrics


class StdScoreDataEnums(Enum):

    TIME          = 0
    POS           = 1
    HIT_OFFSET    = 2
    POS_OFFSET    = 3
    HITOBJECT_IDX = 4


class StdScoreData():
    """
    Class used for analyzing score data pertaining to a specific play.
    """

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

    """
    Disables hitting next note too early. If False, the neg_miss_range of the current note is 
    overridden to extend to the previous note's pos_hit_range boundary.
    """
    notelock = True

    """
    Overrides the miss and hit windows to correspond to spacing between notes. If True then all 
    the ranges are are overridden to be split up in 1/4th sections relative to the distance between 
    current and next notes
    """
    dynamic_window = False

    """
    Enables missing in blank space. If True, the Nothing window behaves like the miss window, but the 
    iterator does not go to the next note.
    """
    blank_miss = False

    """
    If True, remove release miss window for sliders. This allows to hit sliders and release them whenever
    """
    lazy_sliders = False

    """
    There are cases for which parts of the hitwindow of multiple notes may overlap. If True, all 
    overlapped miss parts are processed for one key event. If False, each overlapped miss part is 
    processed for each individual key event.
    """
    overlap_miss_handling = False

    """
    There are cases for which parts of the hitwindow of multiple notes may overlap. If True, all 
    overlapped hit parts are processed for one key event. If False, each overlapped hit part is 
    processed for each individual key event.
    """
    overlap_hit_handling  = False

    @staticmethod
    def get_score_data(replay_data, map_data):
        """
        Returns data pertaining to player's timing on notes in the map. This also records any extra taps the player
        may have made

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        map_data : numpy.array
            Map data

        Returns
        -------
        numpy.array
            Score data has time the hit occured, cursor position when the hit occured, hit offset from 0ms, 
            position offset from center of the note, and the idx of the note the hit pertains to.
            ::
                [
                    [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
                    [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
                    [ time, (cursor_pos_x, cursor_pos_y), hit_offset, (pos_offset_x, pos_offset_y), hitobject_idx ],
                    ...  N events
                ]

            If the note is never hit, then the event will be
            ::
                [ time, (cursor_pos_x, cursor_pos_y), float(StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range), (np.nan, np.nan), hitobject_idx ]

            If the tap doesn't hit anything, the event will be
            ::
                [ press_time, cursor_cor, np.nan, (np.nan, np.nan), np.nan ]
        """
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
                        score_data.append([ press_time, cursor_cor, np.nan, (np.nan, np.nan), np.nan ])
                    curr_key_event_idx = idx + 1  # consume event
                    continue                      # next key press

                # Way late taps. Doesn't matter where, ignore these
                is_in_pos_nothing_range = time_offset > pos_nothing_range
                if is_in_pos_nothing_range:
                    if StdScoreData.blank_miss:
                        score_data.append([ press_time, cursor_cor, np.nan, (np.nan, np.nan), np.nan ])
                    curr_key_event_idx = idx + 1  # consume event
                    continue                      # next key press

                # Early miss tap if on circle
                is_in_neg_miss_range = time_offset < -StdScoreData.neg_hit_range
                if is_in_neg_miss_range:
                    if pos_offset < StdScoreData.hitobject_radius:
                        score_data.append([ press_time, cursor_cor, -float(StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range), cursor_cor - aimpoint_cor, hitobject_idx ])
                        curr_key_event_idx    = idx + 1      # consume event
                        is_hitobject_consumed = True; break  # consume hitobject

                # Late miss tap if on circle
                is_in_pos_miss_range = time_offset > StdScoreData.pos_hit_range
                if is_in_pos_miss_range:
                    if pos_offset < StdScoreData.hitobject_radius:
                        score_data.append([ press_time, cursor_cor, float(StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range), cursor_cor - aimpoint_cor, hitobject_idx ])
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
                score_data.append([ aimpoint_time, aimpoint_cor, float(StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range), (np.nan, np.nan), hitobject_idx ])

        return np.asarray(score_data)


    @staticmethod
    def get_velocity_jump_frames(replay_data, map_data):
        """
        Extracts frames of replay data associated with jumps 
        A frame spans from halfway before the last note to halfway after current note

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        map_data : numpy.array
            Map data

        Returns
        -------
        numpy.array
        """
        vel_times, vel_data = StdReplayMetrics.cursor_velocity(replay_data)
        map_times = StdMapData.start_end_times(map_data)
        frames = []

        threshold_vel = vel_data[vel_data != np.inf][int(len(vel_data)*0.8)]
        #vel_data = np.convolve(vel_data, np.ones(3, dtype=float)/3, 'valid')

        for idx in range(1, len(map_times)):
            # Frame start and end
            time_start, time_end = map_times[idx - 1][-1], map_times[idx][0]

            # If it's a slider, expand the frame back a bit
            # Sliders have some leniency allowing the player to leave it before it's fully finished
            # There is a time when it's optimal to leave the slider based on OD (values are fudged for now,
            # but do approach circle OD calc later). 
            if map_times[idx - 1][0] != map_times[idx - 1][-1]:
                time_start -= min((map_times[idx - 1][-1] - map_times[idx - 1][0])*0.5, 50)

            # Get replay data mask spanning that time period
            frame_mask = np.where(np.logical_and(time_start <= vel_times, vel_times <= time_end))[0]

            vel_frame = vel_data[frame_mask]
            if np.all(vel_frame < threshold_vel):
                continue

            time_frame = vel_times[frame_mask]
            #time_frame = time_frame - time_frame[0]

            frames.append([ time_frame, vel_frame ])

        return np.asarray(frames)



    @staticmethod
    def press_interval_mean(score_data):
        # TODO need to put in release offset into score_data
        # TODO need to go through hitobjects and filter out hold notes
        #  
        pass


    @staticmethod
    def tap_offset_mean(score_data):
        """
        Average of tap offsets

        Parameters
        ----------
        score_data : numpy.array
            Score data

        Returns
        -------
        float
        """
        hit_offsets = score_data[:, StdScoreDataEnums.HIT_OFFSET.value]
        
        hit_offsets[hit_offsets == float('inf')]  = StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range
        hit_offsets[hit_offsets == float('-inf')] = -(StdScoreData.neg_hit_range + StdScoreData.neg_hit_miss_range)
        hit_offsets = hit_offsets[~np.isnan(hit_offsets.astype(float))]

        return np.mean(hit_offsets)


    @staticmethod
    def tap_offset_var(score_data):
        """
        Variance of tap offsets

        Parameters
        ----------
        score_data : numpy.array
            Score data

        Returns
        -------
        float
        """
        hit_offsets = score_data[:, StdScoreDataEnums.HIT_OFFSET.value]
        
        hit_offsets[hit_offsets == float('inf')]  = StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range
        hit_offsets[hit_offsets == float('-inf')] = -(StdScoreData.neg_hit_range + StdScoreData.neg_hit_miss_range)
        hit_offsets = hit_offsets[~np.isnan(hit_offsets.astype(float))]

        return np.var(hit_offsets)


    @staticmethod
    def tap_offset_stdev(score_data):
        """
        Standard deviation of tap offsets

        Parameters
        ----------
        score_data : numpy.array
            Score data

        Returns
        -------
        float
        """
        hit_offsets = score_data[:, StdScoreDataEnums.HIT_OFFSET.value]
        
        hit_offsets[hit_offsets == float('inf')]  = StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range
        hit_offsets[hit_offsets == float('-inf')] = -(StdScoreData.neg_hit_range + StdScoreData.neg_hit_miss_range)
        hit_offsets = hit_offsets[~np.isnan(hit_offsets.astype(float))]

        return np.std(hit_offsets)


    @staticmethod
    def cursor_pos_offset_mean(score_data):
        """
        Average of cursor position offsets at moments the player tapped notes

        Parameters
        ----------
        score_data : numpy.array
            Score data

        Returns
        -------
        float
        """
        positions = np.stack(score_data[:, StdScoreDataEnums.POS_OFFSET.value], axis=0)
        if not all(np.isnan(positions.flatten())):
            nan_mask = np.isnan(positions)
            nan_mask = ~np.logical_or(nan_mask[:,0], nan_mask[:,1])
            positions = positions[nan_mask]

        return np.mean(positions, axis=0)


    @staticmethod
    def cursor_pos_offset_var(score_data):
        """
        Variance of cursor position offsets at moments the player tapped notes

        Parameters
        ----------
        score_data : numpy.array
            Score data

        Returns
        -------
        float
        """
        positions = np.stack(score_data[:, StdScoreDataEnums.POS_OFFSET.value], axis=0)
        if not all(np.isnan(positions.flatten())):
            nan_mask = np.isnan(positions)
            nan_mask = ~np.logical_or(nan_mask[:,0], nan_mask[:,1])
            positions = positions[nan_mask]

        return np.var(positions, axis=0)


    @staticmethod
    def cursor_pos_offset_stdev(score_data):
        """
        Standard deviation of cursor position offsets at moments the player tapped notes

        Parameters
        ----------
        score_data : numpy.array
            Score data

        Returns
        -------
        float
        """
        positions = np.stack(score_data[:, StdScoreDataEnums.POS_OFFSET.value], axis=0)
        if not all(np.isnan(positions.flatten())):
            nan_mask = np.isnan(positions)
            nan_mask = ~np.logical_or(nan_mask[:,0], nan_mask[:,1])
            positions = positions[nan_mask]

        return np.std(positions, axis=0)


    @staticmethod
    def odds_some_tap_within(score_data, offset):
        """
        Creates a gaussian distribution model using avg and var of tap offsets and calculates the odds that some hit
        is within the specified offset

        Parameters
        ----------
        score_data : numpy.array
            Score data

        offset : float
            Tap offset (ms) to determine odds for

        Returns
        -------
        float
            Probability one random value ``[X]`` is between ``-offset <= X <= offset``.
            In simpler terms, look at all the hits for scores; What are the odds 
            of you picking a random hit that is between ``-offset`` and ``offset``?
        """
        mean  = StdScoreData.tap_offset_mean(score_data)
        stdev = StdScoreData.tap_offset_stdev(score_data)

        prob_less_than_neg = scipy.stats.norm.cdf(-offset, loc=mean, scale=stdev)
        prob_less_than_pos = scipy.stats.norm.cdf(offset, loc=mean, scale=stdev)

        return prob_less_than_pos - prob_less_than_neg


    @staticmethod
    def odds_some_cursor_within(score_data, offset):
        """
        Creates a 2D gaussian distribution model using avg and var of cursor 2D position offsets and uses it to calculates the odds 
        that some cursor position is within the specified distance from the center of any hitobject

        Parameters
        ----------
        score_data : numpy.array
            Score data

        offset : float
            Tap offset (ms) to determine odds for

        Returns
        -------
        float
            Probability one random value ``[X, Y]`` is between ``(-offset, -offset) <= (X, Y) <= (offset, offset)``.
            In simpler terms, look at all the cursor positions for score; What are the odds of you picking a random hit that has 
            a cursor position between an area of ``(-offset, -offset)`` and ``(offset, offset)``?
        """ 
        positions = np.stack(score_data[:, StdScoreDataEnums.POS_OFFSET.value], axis=0)
        if not all(np.isnan(positions.flatten())):
            nan_mask = np.isnan(positions)
            nan_mask = ~np.logical_or(nan_mask[:,0], nan_mask[:,1])
            positions = positions[nan_mask]
        else: return np.nan

        mean_2d = StdScoreData.cursor_pos_offset_mean(score_data)
        if any(np.isnan(mean_2d)): return np.nan

        covariance   = np.cov(positions.T)
        distribution = scipy.stats.multivariate_normal(mean_2d, covariance)

        prob_less_than_neg = distribution.cdf(np.asarray([-offset, -offset]))
        prob_less_than_pos = distribution.cdf(np.asarray([offset, offset]))

        return prob_less_than_pos - prob_less_than_neg


    @staticmethod
    def odds_all_tap_within(score_data, offset):
        """
        Creates a gaussian distribution model using avg and var of tap offsets and calculates the odds that all hits
        are within the specified offset

        Parameters
        ----------
        score_data : numpy.array
            Score data

        offset : float
            Tap offset (ms) to determine odds for

        Returns
        ------- 
        float
            Probability all random values ``[X]`` are between ``-offset <= X <= offset``.
            In simpler terms, look at all the hits for scores; What are the odds all of them are between -offset and offset?
        """
        return StdScoreData.odds_some_tap_within(score_data, offset)**len(score_data)


    @staticmethod
    def odds_all_cursor_within(score_data, offset):    
        """
        Creates a 2D gaussian distribution model using avg and var of cursor 2D position offsets and uses it to calculates the odds 
        that all cursor positions are within the specified distance from the center of all hitobject

        Parameters
        ----------
        score_data : numpy.array
            Score data

        offset : float
            Tap offset (ms) to determine odds for

        Returns
        -------
        float
            Probability all random values ``{[X, Y], ...}`` are between ``(-offset, -offset) <= (X, Y) <= (offset, offset)``
            In simpler terms, look at all the cursor positions for score; What are the odds all of them are between an area 
            of ``(-offset, -offset)`` and ``(offset, offset)``?
        """
        return StdScoreData.odds_some_cursor_within(score_data, offset)**len(score_data)


    @staticmethod
    def odds_all_conditions_within(score_data, tap_offset, cursor_offset):
        """
        Creates gaussian distribution models using tap offsets and cursor offsets for hits. That is used to calculate the odds
        of the player consistently tapping and aiming within those boundaries for the entire play. Be weary of survivorship bias.

        Parameters
        ----------
        score_data : numpy.array
            Score data

        tap_offset : float
            Tap offset (ms) to determine odds for

        cursor_offset : float
            Cursor offset (ms) to determine odds for

        Returns
        -------
        float
        """
        odds_all_tap_within    = StdScoreData.odds_all_tap_within(score_data, tap_offset)
        odds_all_cursor_within = StdScoreData.odds_all_cursor_within(score_data, cursor_offset)

        return odds_all_tap_within*odds_all_cursor_within