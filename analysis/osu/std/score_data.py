from enum import Enum
import numpy as np
import pandas as pd
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

    TYPE_HITP  = 0  # A hit press has a hitobject and offset associated with it
    TYPE_HITR  = 1  # A hit release has a hitobject and offset associated with it
    TYPE_AIMH  = 2  # A hold has an aimpoint and offset associated with it
    TYPE_MISS  = 3  # A miss has a hitobject associated with it, but not offset
    TYPE_EMPTY = 4  # An empty has neither hitobject nor offset associated with it

    DATA_OFFSET  = 0 
    DATA_TYPE    = 1
    DATA_MAP_IDX = 2

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
    Disables hit processing if hit on a note is too early. If False, the neg_miss_range of the current note is 
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
    iterator does not go to the next note. Also allows missing when clicked in empty space.
    """
    blank_miss = False

    """
    If True, release timing processing is not done for sliders. This allows to hit sliders and release them whenever,
    basically treating them as single notes.
    """
    lazy_sliders = False

    """
    If True, sliders can be released and then pressed again so long as player holds key down when an aimpoint
    is passed. If false, then upon release all aimpoints that follow are dropped and note's release timing is processed
    """
    recoverable_release = True

    """
    If True, the cursor can wander off slider and come back so long as the cursor is there when it's time for the aimpoint
    to be processed. If False, then slider release timing is triggered as soon as the cursor is out of range 
    """
    recoverable_missaim = True

    """
    There are cases for which parts of the hitwindow of multiple notes may overlap. If True, all 
    overlapped miss hitwindow sections are all processed simultaniously for one key event. If 
    False, each overlapped miss part is processed for each individual key event.
    """
    overlap_miss_handling = False

    """
    There are cases for which parts of the hitwindow of multiple notes may overlap. If True, all 
    overlapped non miss hitwindow parts are all processed simultaniously for one key event. If 
    False, each overlapped hit part is processed for each individual key event.
    """
    overlap_hit_handling = False

    """
    If true then presses while holding another key will not register
    """
    press_block = False

    """
    If true then releases while holding another key will not register
    """
    release_block = True


    @staticmethod
    def __get_key_state(master_key_state, key_states, press_block=False, release_block=True):
        """
        Since std has 4 buttons that are essentially treat as one key,
        the 4 states need to be processed and merged into one state.

        Parameters
        ----------
        master_key_state : int
            The current state of the one merged key

        key_states : numpy.array
            The states of each individual key

        Returns
        -------
        int
            The resultant state of the master key
        """
        key_states = np.asarray(key_states)

        # If new state has a press
        if any(key_states == StdReplayData.PRESS):
            press_reg = True
            if press_block:  # Make sure player is not holding a key already
                press_reg &= master_key_state != StdReplayData.HOLD
            if press_reg:
                return StdReplayData.PRESS

        if any(key_states == StdReplayData.RELEASE):
            release_reg = True
            if release_block:  # Make sure player is not holding a key already
                release_reg = master_key_state != StdReplayData.HOLD
            release_reg &= (master_key_state != StdReplayData.FREE)
            if release_reg:
                return StdReplayData.RELEASE

        if any(key_states == StdReplayData.HOLD) or (master_key_state == StdReplayData.HOLD):
            return StdReplayData.HOLD

        return StdReplayData.FREE


    @staticmethod
    def get_score_data(replay_data, map_data, ar=8, cs=4):
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
                    [ aimpoint_time, cursor_pos_x, cursor_pos_y, aimpoint_x, aimpoint_y, score_type, map_idx ],
                    [ aimpoint_time, cursor_pos_x, cursor_pos_y, aimpoint_x, aimpoint_y, score_type, map_idx ],
                    [ aimpoint_time, cursor_pos_x, cursor_pos_y, aimpoint_x, aimpoint_y, score_type, map_idx ],
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

        # Score data that will be filled in and returned
        score_data = {}

        # Note and reply pointers
        note_idx = 0
        replay_idx = 0

        # Number of things to loop through
        num_hitobjects = StdMapData.get_num_hitobjects(map_data)
        num_replay_events = len(replay_data)

        # Key state
        key_state = StdReplayData.FREE
        
        # Keep track of time we are in the map. This basically simulates
        # normal map playback, but skipping to points in time that actually matter
        # It also plays a role keeping track of map-replay sync
        psuedo_time = None

        # Keep track of whether the note has been consumed or not
        note_consumed = False

        # Go through each note
        while True:
            # Condition checks whether we processed all notes
            if note_idx >= num_hitobjects: break

            # If note is consumed, go to next one
            if note_consumed:
                note_idx += 1
                note_consumed = False
                note_pressed = False
                continue

            # Aimpoint data
            aimpoints = map_data.loc[note_idx]
            num_aimpoints = len(aimpoints)
            aimpoint_idx = 0

            # Note start and end params
            note_start_time = aimpoints.iloc[0].name
            note_start_xcor = aimpoints.iloc[0]['x']
            note_start_ycor = aimpoints.iloc[0]['y']

            note_end_time = aimpoints.iloc[-1].name
            note_end_xcor = aimpoints.iloc[-1]['x']
            note_end_ycor = aimpoints.iloc[-1]['y']

            # Is current note a single note?
            is_single_note = ((note_end_time - note_start_time) <= 1)

            # Keeping track whether the note got pressed
            note_pressed = False

            # Go through each aimpoint
            while True:
                # Condition checks whether we processed all aimpoints
                if aimpoint_idx >= num_aimpoints:
                    note_consumed = True
                    break

                # Advance note_idx before continuing going through aimpoint_idx
                if note_consumed: break

                # Get aimpoint timings and positions
                aim_time = aimpoints.iloc[aimpoint_idx].name
                aim_xcor = aimpoints.iloc[aimpoint_idx]['x']
                aim_ycor = aimpoints.iloc[aimpoint_idx]['y']

                aimpoint_idx += 1
                
                # Go through replay events
                while True:
                    # Condition check whether all player actions in the column have been processed
                    # It's possible that the player never pressed any keys, so this may hit more
                    # often than one may expect
                    if replay_idx >= num_replay_events: break

                    # Advance note_idx before continuing going through replay_idx
                    if note_consumed: break

                    # Time of event frame
                    replay_time = replay_data.index[replay_idx]

                    # Position of the cursor at event frame
                    replay_xpos = replay_data.iloc[replay_idx]['x']
                    replay_ypos = replay_data.iloc[replay_idx]['y']

                    # Press states at event frame
                    replay_keys = replay_data.iloc[replay_idx][[ 'm1', 'm2', 'k1', 'k2' ]]
                    key_state = StdScoreData.__get_key_state(key_state, replay_keys)

                    replay_idx += 1

                    # Nothing to calc if the player is not pressing on anything
                    if key_state == StdReplayData.FREE:
                        # if replay is ahead of a note timing
                        # that has not yet been consumed, the timing is considered missed
                        if not note_pressed:
                            time_offset = replay_time - note_start_time
                            is_in_pos_miss_range = time_offset > StdScoreData.pos_hit_range

                            # Missed starting point by not pressing
                            if is_in_pos_miss_range:
                                score_data[replay_time] = np.asarray([ note_start_time, np.nan, np.nan, note_start_xcor, note_start_ycor, StdScoreData.TYPE_MISS, note_idx ])
                                note_consumed = True
                                break
                        else:
                            # Missed ending point by note pressing
                            if replay_time > note_end_time:
                                score_data[replay_time] = np.asarray([ note_end_time, np.nan, np.nan, note_start_xcor, note_start_ycor, StdScoreData.TYPE_MISS, note_idx ])
                                note_consumed = True
                                break

                        continue

                    if key_state == StdReplayData.PRESS:
                        # If note has already been pressed, that it must
                        # either be held down or released
                        if note_pressed == True:
                            continue

                        # Calc offsets between player and map
                        time_offset = replay_time - note_start_time
                        posx_offset = replay_xpos - note_start_xcor
                        posy_offset = replay_ypos - note_start_ycor
                        pos_offset  = (posx_offset**2 + posy_offset**2)**0.5

                        # Miss hit, not in circle
                        if pos_offset > StdScoreData.hitobject_radius:
                            # blank miss is on -> record empty miss, otherwise ignore
                            if StdScoreData.blank_miss:
                                score_data[replay_time] = np.asarray([ np.nan, replay_xpos, replay_ypos, np.nan, np.nan, StdScoreData.TYPE_EMPTY, None ])
                            continue

                        # Stuff after this is within circle

                        # Way early taps
                        is_in_neg_nothing_range = time_offset < -neg_nothing_range
                        if is_in_neg_nothing_range:
                            # blank miss is on -> record empty miss, otherwise ignore
                            if StdScoreData.blank_miss:
                                score_data[replay_time] = np.asarray([ np.nan, replay_xpos, replay_ypos, np.nan, np.nan, StdScoreData.TYPE_EMPTY, None ])
                            continue

                        # Way late taps. Doesn't matter where, ignore these
                        is_in_pos_nothing_range = time_offset > pos_nothing_range
                        if is_in_pos_nothing_range:
                            continue

                        # Early miss tap
                        is_in_neg_miss_range = time_offset < -StdScoreData.neg_hit_range
                        if is_in_neg_miss_range:
                            score_data[replay_time] = np.asarray([ note_start_time, replay_xpos, replay_ypos, note_start_xcor, note_start_ycor, StdScoreData.TYPE_MISS, note_idx ])
                            
                            # Consume if single note
                            if is_single_note: note_consumed = True
                            break  # advance aimpoint_idx

                        # Late miss tap
                        is_in_pos_miss_range = time_offset > StdScoreData.pos_hit_range
                        if is_in_pos_miss_range:
                            score_data[replay_time] = np.asarray([ note_start_time, replay_xpos, replay_ypos, note_start_xcor, note_start_ycor, StdScoreData.TYPE_MISS, note_idx ])
                            
                            # Consume if single note
                            if is_single_note: note_consumed = True
                            break  # advance aimpoint_idx

                        # If none of the above, then it's a hit
                        score_data[replay_time] = np.asarray([ note_start_time, replay_xpos, replay_ypos, note_start_xcor, note_start_ycor, StdScoreData.TYPE_HITP, note_idx ])

                        # Consume if single note, otherwise mark that it's pressed
                        if is_single_note: 
                            note_consumed = True
                        else: 
                            note_pressed = True
                            
                        break  # advance aimpoint_idx

                    # If a release occurs at this time
                    if key_state == StdReplayData.RELEASE:
                        # Note has to be pressed before it can be released
                        if not note_pressed: continue

                        # If this is true, then release timings are ignored
                        if StdScoreData.lazy_sliders:
                            note_consumed = True
                            break  # advance aimpoint_idx

                        # Calc offsets between player and map
                        time_offset = replay_time - note_end_time
                        posx_offset = replay_xpos - note_end_xcor
                        posy_offset = replay_ypos - note_end_ycor
                        pos_offset  = (posx_offset**2 + posy_offset**2)**0.5

                        # TODO: Process release timings

                        # If none of the above, then it's a hit
                        score_data[replay_time] = np.asarray([ note_end_time, replay_xpos, replay_ypos, note_end_xcor, note_end_ycor, StdScoreData.TYPE_HITR, note_idx ])

                        # Note has been released and finished
                        note_consumed = True
                        break                        

                    # If a hold occurs at this time
                    if key_state == StdReplayData.HOLD:
                        posx_offset = replay_xpos - aim_xcor
                        posy_offset = replay_ypos - aim_ycor
                        pos_offset  = (posx_offset**2 + posy_offset**2)**0.5

                        # Aimpoints don't count if cursor not within range
                        if pos_offset > StdScoreData.follow_radius:
                            if not StdScoreData.recoverable_release:
                                score_data[replay_time] = np.asarray([ note_end_time, replay_xpos, replay_ypos, note_end_xcor, note_end_ycor, StdScoreData.TYPE_HITR, note_idx ])
                            continue

                        # TODO: Process aimpoints

                        # If replay at or passed aimpoint, then advance aimpoint_idx
                        if replay_time >= aim_time:
                            score_data[replay_time] = np.asarray([ aim_time, replay_xpos, replay_ypos, aim_xcor, aim_ycor, StdScoreData.TYPE_AIMH, note_idx ])
                            break

                        # Otherwise, keeping going through replay
                        continue

        # Sort data by timings
        score_data = dict(sorted(score_data.items()))

        # Convert the dictionary of recorded timings and states into a pandas data
        score_data = pd.DataFrame.from_dict(score_data, orient='index', columns=['map_t', 'replay_x', 'replay_y', 'map_x', 'map_y', 'type', 'map_idx'])
        score_data.index.name = 'replay_t'
        return score_data


    '''
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
    '''


    @staticmethod
    def tap_press_offsets(score_data):
        hit_presses = score_data.query(f'type == {StdScoreData.TYPE_HITP}')
        return hit_presses['map_t'] - hit_presses.index.values


    @staticmethod
    def tap_release_offsets(score_data):
        hit_releases = score_data.query(f'type == {StdScoreData.TYPE_HITR}')
        return hit_releases['map_t'] - hit_releases.index.values


    @staticmethod
    def aim_x_offsets(score_data):
        hit_presses = score_data.query(f'type == {StdScoreData.TYPE_HITP}')
        return hit_presses['map_x'] - hit_presses['replay_x']


    @staticmethod
    def aim_y_offsets(score_data):
        hit_presses = score_data.query(f'type == {StdScoreData.TYPE_HITP}')
        return hit_presses['map_y'] - hit_presses['replay_y']


    @staticmethod
    def aim_offsets(score_data):
        hit_presses = score_data.query(f'type == {StdScoreData.TYPE_HITP}')
        offset_x = hit_presses['map_x'] - hit_presses['replay_x']
        offset_y = hit_presses['map_y'] - hit_presses['replay_y']
        return (offset_x**2 + offset_y**2)**0.5


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
        return np.mean(StdScoreData.tap_press_offsets(score_data))


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
        return np.var(StdScoreData.tap_press_offsets(score_data))


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
        return np.std(StdScoreData.tap_press_offsets(score_data))


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
        return np.mean(StdScoreData.aim_offsets(score_data))


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
        return np.var(StdScoreData.aim_offsets(score_data))


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
        return np.std(StdScoreData.aim_offsets(score_data))


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

        # scipy cdf can't handle 0 stdev (div by 0)
        if stdev == 0:
            return 1.0 if -offset <= mean <= offset else 0.0

        prob_greater_than_neg = scipy.stats.norm.cdf(-offset, loc=mean, scale=stdev)
        prob_less_than_pos = scipy.stats.norm.cdf(offset, loc=mean, scale=stdev)

        return prob_less_than_pos - prob_greater_than_neg


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
        aim_x_offsets = StdScoreData.aim_x_offsets(score_data)
        aim_y_offsets = StdScoreData.aim_y_offsets(score_data)

        mean_aim_x = np.mean(aim_x_offsets)
        mean_aim_y = np.mean(aim_y_offsets)

        mean = np.asarray([ mean_aim_x, mean_aim_y ])
        covariance = np.cov(np.asarray([ aim_x_offsets, aim_y_offsets ]))
        
        distribution = scipy.stats.multivariate_normal(mean, covariance, allow_singular=True)

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
        # TODO: handle misses
        
        hit_presses = score_data.query(f'type == {StdScoreData.TYPE_HITP}')
        return StdScoreData.odds_some_tap_within(score_data, offset)**len(hit_presses)


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
        # TODO: handle misses

        hit_presses = score_data.query(f'type == {StdScoreData.TYPE_HITP}')
        return StdScoreData.odds_some_cursor_within(score_data, offset)**len(hit_presses)


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