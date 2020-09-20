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

import time


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
    __ADV_NOP  = 0  # Used internal by scoring processor; Don't advance
    __ADV_AIMP = 1  # Used internal by scoring processor; Advance to next aimpoint
    __ADV_NOTE = 2  # Used internal by scoring processor; Advance to next note

    TYPE_HITP  = 0  # A hit press has a hitobject and offset associated with it
    TYPE_HITR  = 1  # A hit release has a hitobject and offset associated with it
    TYPE_AIMH  = 2  # A hold has an aimpoint and offset associated with it
    TYPE_MISS  = 3  # A miss has a hitobject associated with it, but not offset
    TYPE_EMPTY = 4  # An empty has neither hitobject nor offset associated with it

    DATA_OFFSET  = 0 
    DATA_TYPE    = 1
    DATA_MAP_IDX = 2

    '''
    The following must be true:
        0 < pos_hit_range < pos_hit_miss_range < inf
        0 < neg_hit_range < neg_hit_miss_range < inf

    Hit processing occurs:
        -neg_hit_range -> pos_hit_range

    Miss processing occurs:
        -neg_hit_miss_range -> neg_hit_range
        pos_hit_range -> pos_hit_miss_range

    No processing occurs:
        -inf -> -neg_hit_miss_range
        pos_hit_miss_range -> inf
    '''
    pos_hit_range      = 300    # ms point of late hit window
    neg_hit_range      = 300    # ms point of early hit window
    pos_hit_miss_range = 450    # ms point of late miss window
    neg_hit_miss_range = 450    # ms point of early miss window

    pos_rel_range       = 500   # ms point of late release window
    neg_rel_range       = 500   # ms point of early release window
    pos_rel_miss_range  = 1000  # ms point of late release window
    neg_rel_miss_range  = 1000  # ms point of early release window

    neg_hld_range   = 50     # ms range of early hold
    pos_hld_range   = 1000   # ms range of late hold

    dist_miss_range = 50   # ms range the cursor can deviate from aimpoint distance threshold before it's a miss

    hitobject_radius = Std.cs_to_px(4)  # Radius from hitobject for which cursor needs to be within for a tap to count
    follow_radius    = 100  # Radius from slider aimpoint for which cursor needs to be within for a hold to count
    release_radius   = 100  # Radius from release aimpoint for which cursor needs to be within for a release to count

    """
    Disables hit processing if hit on a note is too early. If False, the neg_miss_range of the current note is 
    overridden to extend to the previous note's pos_hit_range boundary.

    TODO: implement
    """
    notelock = True

    """
    Overrides the miss and hit windows to correspond to spacing between notes. If True then all 
    the ranges are are overridden to be split up in 1/4th sections relative to the distance between 
    current and next notes

    TODO: implement
    """
    dynamic_window = False

    """
    Enables missing in blank space. If True, the Nothing window behaves like the miss window, but the 
    iterator does not go to the next note. Also allows missing when clicked in empty space.
    """
    blank_miss = False

    """
    If True, holds have to be times in distance range of HOLD scorepoint prior to completing it
    If False, the player can complete the slider with cursor being anywhere so long as the key is held down
    """
    hold_range_window = False

    """
    If True,  holds have to be times in distance range of HOLD scorepoint prior to completing it or it will miss
    If False, the scorepoint won't be completed until the cursor is in distance range of scorepoint
    
    hold_range_window must be True for this to take effect
    """
    hold_range_miss = False

    """
    If True, sliders can be released and then pressed again so long as player holds key down when an aimpoint
    is passed. If false, then upon release all aimpoints that follow are dropped and note's release timing is processed
    """
    recoverable_release = True

    """
    If True, release have to be in range of RELEASE scorepoint to count
    """
    release_range = False

    """
    If True, release miss range is processed. Otherwise, it's impossible to miss a release
    """
    release_miss = True

    """
    If True, then there is a release window. Otherwise, a release can be counted whenever 
    key is released, basically treating them as single notes. Also if True, release_miss does nothing
    """
    release_window = True

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
    release_block = False


    @staticmethod
    def __adv(map_data, map_time, adv):
        if adv == StdScoreData.__ADV_NOP:
            return map_time

        if adv == StdScoreData.__ADV_AIMP:
            aimpoint = StdMapData.get_scorepoint_after(map_data, map_time)
            if type(aimpoint) == type(None): 
                return StdMapData.all_times(map_data)[-1] + 1
            
            return aimpoint['time']

        if adv == StdScoreData.__ADV_NOTE:
            note = StdMapData.get_note_after(map_data, map_time)
            if type(note) == type(None):
                return StdMapData.all_times(map_data)[-1] + 1
            return note['time'][0]

        return map_time


    @staticmethod
    def __process_free(score_data, visible_notes, replay_time, replay_xpos, replay_ypos):
        note_idx = visible_notes.index[0][0]

        # Aimpoint data
        aimpoints = visible_notes.values

        # Note start and end params
        aimpoint_time = aimpoints[0][0]  # time
        aimpoint_xcor = aimpoints[0][1]  # x
        aimpoint_ycor = aimpoints[0][2]  # y
        aimpoint_type = aimpoints[0][3]  # type

        # Free only looks at timings that have passed
        if replay_time <= aimpoint_time:
            return StdScoreData.__ADV_NOP

        time_offset = replay_time - aimpoint_time
        posx_offset = replay_xpos - aimpoint_xcor
        posy_offset = replay_ypos - aimpoint_ycor
        pos_offset  = (posx_offset**2 + posy_offset**2)**0.5

        is_in_pos_nothing_range = False

        # Missed note by not pressing or missaiming
        if aimpoint_type == StdMapData.TYPE_PRESS:   
            is_in_pos_nothing_range = time_offset > StdScoreData.pos_hit_miss_range

        if aimpoint_type == StdMapData.TYPE_RELEASE:
            if StdScoreData.release_window:
                is_in_pos_nothing_range = time_offset > StdScoreData.pos_rel_miss_range
            else:
                return StdScoreData.__ADV_NOP

        if aimpoint_type == StdMapData.TYPE_HOLD:
            # Recoverable missaim check
            if not StdScoreData.recoverable_missaim:
                # If recoverable missaim is off, then wandering off the follow radius is a miss
                if pos_offset > StdScoreData.follow_radius:
                    score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, np.nan, np.nan, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_MISS, StdReplayData.FREE, note_idx ])
                    return StdScoreData.__ADV_NOTE

            # Recoverable release check
            if StdScoreData.recoverable_release:
                # If recoverable release is on, allow some time to repress
                is_in_pos_nothing_range = time_offset > StdScoreData.pos_hld_range
            else:
                is_in_pos_nothing_range = time_offset > 0

        if is_in_pos_nothing_range:
            score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, np.nan, np.nan, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_MISS, StdReplayData.FREE, note_idx ])
            return StdScoreData.__ADV_NOTE

        return StdScoreData.__ADV_NOP


    @staticmethod
    def __process_press(score_data, visible_notes, replay_time, replay_xpos, replay_ypos):
        note_idx = visible_notes.index[0][0]

        # Aimpoint data
        aimpoints = visible_notes.values

        # Note start and end params
        aimpoint_time = aimpoints[0][0]  # time
        aimpoint_xcor = aimpoints[0][1]  # x
        aimpoint_ycor = aimpoints[0][2]  # y
        aimpoint_type = aimpoints[0][3]  # type
        aimpoint_obj  = aimpoints[0][4]  # object

        # If it's not an aimpoint at start of hitobject, ignore
        if aimpoint_type != StdMapData.TYPE_PRESS:
            return StdScoreData.__ADV_NOP

        time_offset = replay_time - aimpoint_time
        posx_offset = replay_xpos - aimpoint_xcor
        posy_offset = replay_ypos - aimpoint_ycor
        pos_offset  = (posx_offset**2 + posy_offset**2)**0.5

        # Miss hit, not in circle
        if pos_offset > StdScoreData.hitobject_radius:
            # Blank Miss check
            if StdScoreData.blank_miss:
                score_data[len(score_data)] = np.asarray([ replay_time, np.nan, replay_xpos, replay_ypos, np.nan, np.nan, StdScoreData.TYPE_EMPTY, StdReplayData.PRESS, None ])
            return StdScoreData.__ADV_NOP

        # Stuff after this is within circle

        # Way early taps
        is_in_neg_nothing_range = time_offset <= -StdScoreData.neg_hit_miss_range
        if is_in_neg_nothing_range:
            # Blank Miss check
            if StdScoreData.blank_miss:
                score_data[len(score_data)] = np.asarray([ replay_time, np.nan, replay_xpos, replay_ypos, np.nan, np.nan, StdScoreData.TYPE_EMPTY, StdReplayData.PRESS, None ])
            return StdScoreData.__ADV_NOP

        # Early miss tap
        is_in_neg_miss_range = -StdScoreData.neg_hit_miss_range < time_offset <= -StdScoreData.neg_hit_range
        if is_in_neg_miss_range:
            score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, replay_xpos, replay_ypos, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_MISS, StdReplayData.PRESS, note_idx ])
            return StdScoreData.__ADV_NOTE

        # Hit window
        is_in_hit_range = -StdScoreData.neg_hit_range < time_offset <= StdScoreData.pos_hit_range
        if is_in_hit_range:
            score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, replay_xpos, replay_ypos, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_HITP, StdReplayData.PRESS, note_idx ])
            if aimpoint_obj == StdMapData.TYPE_SLIDER:
                return StdScoreData.__ADV_AIMP
            else:
                return StdScoreData.__ADV_NOTE

        # Late miss tap
        is_in_pos_miss_range = StdScoreData.pos_hit_range < time_offset <= StdScoreData.pos_hit_miss_range
        if is_in_pos_miss_range:
            score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, replay_xpos, replay_ypos, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_MISS, StdReplayData.PRESS, note_idx ])
            return StdScoreData.__ADV_NOTE

        # Way late taps. Ignore these
        is_in_pos_nothing_range = StdScoreData.pos_hit_miss_range < time_offset
        if is_in_pos_nothing_range:
            return StdScoreData.__ADV_NOP


    @staticmethod
    def __process_hold(score_data, visible_notes, replay_time, replay_xpos, replay_ypos):
        note_idx = visible_notes.index[0][0]

        # Aimpoint data
        aimpoints = visible_notes.values

        # Note start and end params
        aimpoint_time = aimpoints[0][0]  # time
        aimpoint_xcor = aimpoints[0][1]  # x
        aimpoint_ycor = aimpoints[0][2]  # y
        aimpoint_type = aimpoints[0][3]  # type

        # If the scorepoint is not a HOLD, ignore
        if aimpoint_type != StdMapData.TYPE_HOLD:
            return StdScoreData.__ADV_NOP

        time_offset = replay_time - aimpoint_time
        posx_offset = replay_xpos - aimpoint_xcor
        posy_offset = replay_ypos - aimpoint_ycor
        pos_offset  = (posx_offset**2 + posy_offset**2)**0.5

        # Hold range check
        if StdScoreData.hold_range_window:
            if pos_offset > StdScoreData.follow_radius:
                # Hold range miss check
                if StdScoreData.hold_range_miss:
                    score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, replay_xpos, replay_ypos, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_MISS, StdReplayData.HOLD, note_idx ])
                    return StdScoreData.__ADV_NOTE
                else:
                    return StdScoreData.__ADV_NOP
        
        # Too early to count
        if time_offset <= -StdScoreData.neg_hld_range:
            return StdScoreData.__ADV_NOP

        # Hold window
        if -StdScoreData.neg_hld_range < time_offset <= StdScoreData.pos_hld_range:
            score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, replay_xpos, replay_ypos, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_AIMH, StdReplayData.HOLD, note_idx ])
            return StdScoreData.__ADV_AIMP

        # Too late to count
        if StdScoreData.pos_hld_range < time_offset:
            return StdScoreData.__ADV_NOP


    @staticmethod
    def __process_release(score_data, visible_notes, replay_time, replay_xpos, replay_ypos):
        note_idx = visible_notes.index[0][0]

        # Aimpoint data
        aimpoints = visible_notes.values

        # Note start and end params
        aimpoint_time = aimpoints[0][0]  # time
        aimpoint_xcor = aimpoints[0][1]  # x
        aimpoint_ycor = aimpoints[0][2]  # y
        aimpoint_type = aimpoints[0][3]  # type

        # If the scorepoint expects a press, then ignore
        if aimpoint_type == StdMapData.TYPE_PRESS:
            return StdScoreData.__ADV_NOP

        # If the scorepoint expects a hold, 
        # then ignore if the release can be recovered from
        if aimpoint_type == StdMapData.TYPE_HOLD:
            if StdScoreData.recoverable_release:
                return StdScoreData.__ADV_NOP

        time_offset = replay_time - aimpoint_time
        posx_offset = replay_xpos - aimpoint_xcor
        posy_offset = replay_ypos - aimpoint_ycor
        pos_offset  = (posx_offset**2 + posy_offset**2)**0.5

        # Non recoverable release check
        if aimpoint_type == StdMapData.TYPE_HOLD:
            # Releasing when expecting a hold means MISS
            if time_offset < 0:
                score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, replay_xpos, replay_ypos, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_MISS, StdReplayData.HOLD, note_idx ])
                return StdScoreData.__ADV_NOTE
            # Otherwise it's fine
            else:
                return StdScoreData.__ADV_NOP

        # Release range check
        if StdScoreData.release_range:
            # If it's outside distance range, then it's not processed
            if pos_offset > StdScoreData.release_radius:
                return StdScoreData.__ADV_NOP

        # Release window check
        if not StdScoreData.release_window:
            score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, replay_xpos, replay_ypos, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_HITR, StdReplayData.RELEASE, note_idx ])
            return StdScoreData.__ADV_AIMP

        # Way early release
        is_in_neg_nothing_range = time_offset <= -StdScoreData.neg_rel_miss_range
        if is_in_neg_nothing_range:
            return StdScoreData.__ADV_NOP
        
        # Early miss release
        is_in_neg_miss_range = -StdScoreData.neg_rel_miss_range < time_offset <= -StdScoreData.neg_rel_range
        if is_in_neg_miss_range:
            if StdScoreData.release_miss:
                score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, replay_xpos, replay_ypos, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_MISS, StdReplayData.RELEASE, note_idx ])
                return StdScoreData.__ADV_NOTE
            else:
                return StdScoreData.__ADV_NOP

        # Release window
        is_in_rel_range = -StdScoreData.neg_rel_range < time_offset <= StdScoreData.pos_rel_range
        if is_in_rel_range:
            score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, replay_xpos, replay_ypos, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_HITR, StdReplayData.RELEASE, note_idx ])
            return StdScoreData.__ADV_AIMP

        # Late miss release
        is_in_pos_miss_range = StdScoreData.pos_rel_range < time_offset <= StdScoreData.pos_rel_miss_range
        if is_in_pos_miss_range:
            if StdScoreData.release_miss:
                score_data[len(score_data)] = np.asarray([ replay_time, aimpoint_time, replay_xpos, replay_ypos, aimpoint_xcor, aimpoint_ycor, StdScoreData.TYPE_MISS, StdReplayData.RELEASE, note_idx ])
                return StdScoreData.__ADV_NOTE
            else:
                return StdScoreData.__ADV_NOP

        # Way late release
        is_in_pos_nothing_range = StdScoreData.pos_rel_miss_range < time_offset
        if is_in_pos_nothing_range:
            return StdScoreData.__ADV_NOP


    @staticmethod
    def get_score_data(replay_data, map_data, ar=8, cs=4):
        # Score data that will be filled in and returned
        score_data = {}

        # replay pointer
        replay_idx = 0

        # map_time is the time at which hitobject processing logic is at
        map_time = StdMapData.all_times(map_data)[0]

        # Number of things to loop through
        replay_data = StdReplayData.get_reduced_replay_data(replay_data, press_block=StdScoreData.press_block, release_block=StdScoreData.release_block).values
        num_replay_events = len(replay_data)

        # Go through replay events
        while True:
            # Condition check whether all player actions in the column have been processed
            if replay_idx >= num_replay_events: break

            # Data for this event frame
            replay_time = replay_data[replay_idx][0]  # time
            replay_xpos = replay_data[replay_idx][1]  # x
            replay_ypos = replay_data[replay_idx][2]  # y
            replay_key  = replay_data[replay_idx][3]  # keys

            # Got all info at current index, now advance it
            replay_idx += 1

            # Go through map
            while True:
                # Get time of earliest visble hitobject still remaining, but if make sure things that
                # have yet to be processed have been processed (in the case of replay skipping)
                #earliest_visible_time = replay_time - StdScoreData.pos_hit_nothing_range

                start_time = min(map_time, replay_time + Std.ar_to_ms(ar)) - 1
                end_time   = max(map_time, replay_time + Std.ar_to_ms(ar))

                # Get visible notes at current time
                visible_notes = StdMapData.time_slice(map_data, start_time, end_time)

                if len(visible_notes) == 0: break
                if replay_time <= map_time: break

                # Check for any skipped notes (if replay has event gaps)
                adv = StdScoreData.__process_free(score_data, visible_notes, replay_time, replay_xpos, replay_ypos)
                if adv == StdScoreData.__ADV_NOP: break
                map_time = StdScoreData.__adv(map_data, map_time, adv)

            # Nothing to process if no notes are visible
            if len(visible_notes) == 0: continue

            # Process player actions
            if replay_key == StdReplayData.FREE:    map_time = StdScoreData.__adv(map_data, map_time, StdScoreData.__process_free(score_data, visible_notes, replay_time, replay_xpos, replay_ypos))
            if replay_key == StdReplayData.PRESS:   map_time = StdScoreData.__adv(map_data, map_time, StdScoreData.__process_press(score_data, visible_notes, replay_time, replay_xpos, replay_ypos))
            if replay_key == StdReplayData.HOLD:    map_time = StdScoreData.__adv(map_data, map_time, StdScoreData.__process_hold(score_data, visible_notes, replay_time, replay_xpos, replay_ypos))
            if replay_key == StdReplayData.RELEASE: map_time = StdScoreData.__adv(map_data, map_time, StdScoreData.__process_release(score_data, visible_notes, replay_time, replay_xpos, replay_ypos))

        # Convert recorded timings and states into a pandas data
        score_data = list(score_data.values())
        return pd.DataFrame(score_data, columns=['replay_t', 'map_t', 'replay_x', 'replay_y', 'map_x', 'map_y', 'type', 'action', 'map_idx'])


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
        hit_presses = score_data[score_data['type'] == StdScoreData.TYPE_HITP]
        return hit_presses['replay_t'] - hit_presses['map_t']


    @staticmethod
    def tap_release_offsets(score_data):
        hit_releases = score_data[score_data['type'] == StdScoreData.TYPE_HITR]
        return hit_releases['replay_t'] - hit_releases['map_t']


    @staticmethod
    def aim_x_offsets(score_data):
        hit_presses = score_data[score_data['type'] == StdScoreData.TYPE_HITP]
        return hit_presses['replay_x'] - hit_presses['map_x']


    @staticmethod
    def aim_y_offsets(score_data):
        hit_presses = score_data[score_data['type'] == StdScoreData.TYPE_HITP]
        return hit_presses['replay_y'] - hit_presses['map_y']


    @staticmethod
    def aim_offsets(score_data):
        hit_presses = score_data[score_data['type'] != StdScoreData.TYPE_HITR]
        offset_x = hit_presses['replay_x'] - hit_presses['map_x']
        offset_y = hit_presses['replay_y'] - hit_presses['map_y']
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

        hit_presses = score_data[score_data['type'] == StdScoreData.TYPE_HITP]
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

        hit_presses = score_data[score_data['type'] == StdScoreData.TYPE_HITP]
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