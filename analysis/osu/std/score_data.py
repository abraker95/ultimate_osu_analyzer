import numpy as np

from misc.numpy_utils import NumpyUtils
from misc.geometry import get_distance

from osu.local.hitobject.std.std import Std
from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.replay_data import StdReplayData



'''
[
    [ time, (cursor_pos_x, cursor_pos_y), hit_offset, pos_offset, hitobject_idx ],
    [ time, (cursor_pos_x, cursor_pos_y), hit_offset, pos_offset, hitobject_idx ],
    [ time, (cursor_pos_x, cursor_pos_y), hit_offset, pos_offset, hitobject_idx ],
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
    def ddd():
        pass


    @staticmethod
    def get_score_data(replay_data, map_data):

        pos_nothing_range = StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range
        neg_nothing_range = StdScoreData.neg_hit_range + StdScoreData.neg_hit_miss_range

        event_data = StdReplayData.press_start_end_times(replay_data)
        curr_key_event_idx = 0
        score_data = []

        # Go through each hitobject
        for hitobject_idx in range(len(map_data)):
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

                cursor_cor = replay_data[int(press_idx)][1], replay_data[int(press_idx)][2]
                pos_offset = get_distance(cursor_cor, aimpoint_cor)

                #score_data.append([ press_time, cursor_cor, offset, key_event_idx, len(event_data) ])
                
                # Way early taps. Doesn't matter where, is a miss if blank miss is on, otherwise ignore these
                is_in_neg_nothing_range = time_offset < -neg_nothing_range
                if is_in_neg_nothing_range:
                    if StdScoreData.blank_miss:
                        score_data.append([ press_time, cursor_cor, float('nan'), float('nan'), float('nan') ])
                    curr_key_event_idx = idx + 1  # consume event
                    continue                      # next key press

                # Way late taps. Doesn't matter where, ignore these
                is_in_pos_nothing_range = time_offset > pos_nothing_range
                if is_in_pos_nothing_range:
                    if StdScoreData.blank_miss:
                        score_data.append([ press_time, cursor_cor, float('nan'), float('nan'), float('nan') ])
                    curr_key_event_idx = idx + 1  # consume event
                    continue                      # next key press

                # Early miss tap if on circle
                is_in_neg_miss_range = time_offset < -StdScoreData.neg_hit_range
                if is_in_neg_miss_range:
                    if pos_offset < StdScoreData.hitobject_radius:
                        score_data.append([ press_time, cursor_cor, float('-inf'), float('nan'), hitobject_idx ])
                        curr_key_event_idx    = idx + 1      # consume event
                        is_hitobject_consumed = True; break  # consume hitobject

                # Late miss tap if on circle
                is_in_pos_miss_range = time_offset > StdScoreData.pos_hit_range
                if is_in_pos_miss_range:
                    if pos_offset < StdScoreData.hitobject_radius:
                        score_data.append([ press_time, cursor_cor, float('inf'), float('nan'), hitobject_idx ])
                        curr_key_event_idx    = idx + 1      # consume event
                        is_hitobject_consumed = True; break  # consume hitobject

                # If a tap is anything else, it's a hit if on circle
                if pos_offset < StdScoreData.hitobject_radius:
                    score_data.append([ press_time, cursor_cor, time_offset, round(pos_offset, 3), hitobject_idx ])

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
                score_data.append([ aimpoint_time, aimpoint_cor, float(StdScoreData.pos_hit_range + StdScoreData.pos_hit_miss_range), float('nan'), hitobject_idx ])

        return np.asarray(score_data)

