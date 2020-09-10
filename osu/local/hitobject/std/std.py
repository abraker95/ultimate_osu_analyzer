from PyQt5.QtCore import *
from PyQt5.QtGui import *

import math

from misc.math_utils import *
from osu.local.hitobject.hitobject import Hitobject
from misc.callback import callback


class StdSettings():

    view_time_back   = 1000                                # ms
    view_time_ahead  = 0                                   # ms
    cursor_radius    = 1.5                                 # osu!px
    cursor_thickness = 1                                   # osu!px
    cursor_color     = QColor(0, 200, 0, 255)              # rgba
    k1_color         = QColor.fromHsl(32,  255, 128, 255)  # rgba
    k2_color         = QColor.fromHsl(180, 255, 96,  255)  # rgba
    m1_color         = QColor.fromHsl(0,   255, 128, 255)  # rgba
    m2_color         = QColor.fromHsl(120, 255, 96,  255)  # rgba

    @staticmethod
    @callback
    def set_view_time_back(view_time_back):
        StdSettings.view_time_back = view_time_back
        StdSettings.set_view_time_back.emit()


    @staticmethod
    @callback
    def set_view_time_ahead(view_time_ahead):
        StdSettings.view_time_ahead = view_time_ahead
        StdSettings.set_view_time_ahead.emit()


    @staticmethod
    @callback
    def set_cursor_radius(cursor_radius):
        StdSettings.cursor_radius = cursor_radius
        StdSettings.set_cursor_radius.emit()


    @staticmethod
    @callback
    def set_cursor_thickness(cursor_thickness):
        StdSettings.cursor_thickness = cursor_thickness
        StdSettings.set_cursor_thickness.emit()


    @staticmethod
    @callback
    def set_cursor_color(cursor_color):
        StdSettings.cursor_color = cursor_color
        StdSettings.set_cursor_color.emit()


    @staticmethod
    @callback
    def set_k1_color(k1_color):
        StdSettings.k1_color = k1_color
        StdSettings.set_k1_color.emit()


    @staticmethod
    @callback
    def set_k2_color(k2_color):
        StdSettings.k2_color = k2_color
        StdSettings.set_k2_color.emit()


    @staticmethod
    @callback
    def set_m1_color(m1_color):
        StdSettings.m1_color = m1_color
        StdSettings.set_m1_color.emit()


    @staticmethod
    @callback
    def set_m2_color(m2_color):
        StdSettings.m2_color = m2_color
        StdSettings.set_m2_color.emit()



class Std():

    PLAYFIELD_WIDTH  = 512  # osu!px
    PLAYFIELD_HEIGHT = 384  # osu!px

    @staticmethod
    def cs_to_px(cs):
        return (109 - 9*cs)/2   # radius -> osu!px


    @staticmethod
    def px_to_cs(px):
        return 2*(109 - px)/9   # osu!px -> radius


    @staticmethod
    def ar_to_ms(ar):
        if ar <= 5: return 1800 - 120*ar
        else:       return 1950 - 150*ar


    @staticmethod
    def ms_to_ar(ms):
        if ms >= 1200.0: return (1800 - ms) / 120.0
        else:            return (1950 - ms) / 150.0


    @staticmethod
    def od300_to_ms(od):
        return 159 - 12.0*od


    @staticmethod
    def ms_to_od300(ms):
        return (159 - ms)/12.0


    @staticmethod
    def sv_to_vel(sv, bpm):
        return (bpm / 60.0) * sv * 100

    
    @staticmethod
    def approch_circle_to_radius(cs, ar, t):
        return 4*Std.cs_to_px(cs) - 3*Std.cs_to_px(cs) * (t/max(800, Std.ar_to_ms(ar)))


    @staticmethod
    def is_hitobject_type(hitobject_type, compare):
        return hitobject_type & compare > 0


    @staticmethod
    def get_fadein_period(ar_ms, hidden_mod=False):
        if hidden_mod:
            return 0.4 * ar_ms
        else:
            return min(ar_ms, 400)


    @staticmethod
    def get_acc_from_hits(num_300_hits, num_100_hits, num_50_hits, num_misses):
        score_hits  = 50*num_50_hits + 100*num_100_hits + 300*num_300_hits
        score_total = 300*(num_misses + num_50_hits + num_100_hits + num_300_hits)
        return score_hits/score_total


    @staticmethod
    def get_time_range(hitobjects):
        try:    return (hitobjects[0].time, hitobjects[-1].end_time)
        except: return (hitobjects[0].time, hitobjects[-1].time)

        # return (self.hitobjects[0].time, list(self.end_times.keys())[-1])


    # TODO: Factor in hidden mod
    # TODO: This breaks on the following condition, where t is any time value:
    #   hitobject_timings = [ (t , 5t), (2t, 3t), (3t, 4t) ]
    #   Condition: t < time < 2t
    #   Returns: [ ]
    #   Expected: [ 0 ]
    @staticmethod
    def get_hitobjects_visible_at_time(beatmap, time, hidden_mod=False):
        # Need to index the ordered dictionary
        hitobject_end_times_timings = list(beatmap.end_times.keys())
        hitobject_end_times_indices = list(beatmap.end_times.values())

        # Find the hitobjects of interest; get the indices to be worked with
        idx_end_time_soonest   = find(hitobject_end_times_timings, time)
        idx_begin_time_soonest = beatmap.end_times[hitobject_end_times_timings[idx_end_time_soonest]]

        idx_begin_time_latest = find(beatmap.hitobjects, time, lambda hitobject: hitobject.time - Std.ar_to_ms(beatmap.difficulty.ar))
        idx_end_time_latest   = find(hitobject_end_times_indices, idx_begin_time_latest)
        
        # The list of visible hitobjects
        hitobject_list = beatmap.hitobjects[idx_begin_time_soonest : idx_begin_time_latest + 1]

        # Iterate through the list of hitobject end timings between the soonest and latest found end times
        # to see if we missed any hitobjects. This is required since 2B maps can throw end timings out of
        # order such that there can be sliders that start and end before other sliders have finished.
        for timing in hitobject_end_times_timings[idx_end_time_soonest : idx_end_time_latest + 1]:
            hitobject = beatmap.hitobjects[beatmap.end_times[timing]]
            if hitobject.time <= time <= hitobject.get_end_time():
                if not hitobject in hitobject_list: hitobject_list.append(hitobject)

        # Remove hitobjects for which end time passed
        for hitobject in hitobject_list[:]:
            if hitobject.get_end_time() < time:
                hitobject_list.remove(hitobject)
                
        return hitobject_list


    @staticmethod
    def get_hitobjects_visible_at_index(beatmap, index, hidden_mod=False):
        return BeatmapUtil.get_hitobjects_visible_at_time(beatmap, beatmap.hitobjects[index].time, hidden_mod)


    @staticmethod
    def is_visible_at(beatmap, hitobject, time):
        return BeatmapUtil.get_opacity_at(beatmap, hitobject, time) > 0.0
        

    @staticmethod
    def get_opacity_at(beatmap, hitobject, time, hidden_mod=False):
        ar_ms = BeatmapUtil.ar_to_ms(beatmap.ar)
        pre_appear_time = hitobject.time - ar_ms  # Time when the AR goes into effect

        if hidden_mod:
            fadein_duration = 0.4 * ar_ms                        # how long the fadein period is
            fadein_time_end = pre_appear_time + fadein_duration  # When it is fully faded in

            # Fadein period always lasts from preamp time to 40% from preamp time to hit time
            percent_fadein = value_to_percent(pre_appear_time, fadein_time_end, time)
            
            # If it's not fully faded in, then we haven't gotten up to the later stuff 
            if percent_fadein < 1.0: 
                return percent_fadein

            # Else this is fade out period

            # If it's a slider, then the fade out period lasts from when it's fadedin to
            # 70% to the time it the slider ends
            if hitobject.is_hitobject_type(Hitobject.SLIDER):
                fadeout_duration = hitobject.get_last_tick_time - fadein_time_end   #  how long the fadeout period is
            else:
                fadeout_duration = 0.7*(hitobject.time - fadein_time_end)
            
            fadeout_time_end = fadein_time_end + fadeout_duration                   #  When it is fully faded out
            return 1.0 - value_to_percent(fadeout_time_end, fadeout_time_end, time)
        else:
            fadein_duration = min(ar_ms, 400)                      # how long the fadein period is
            fadein_time_end = pre_appear_time + fadein_duration    # When it is fully faded in

            # Fadein period always lasts from preamp time to 400 ms after preamp time or
            # when the object needs to be hit, which ever is smaller
            percent_fadein = value_to_percent(pre_appear_time, fadein_time_end, time)
            
            # If it's not fully faded in, then we haven't gotten up to the later stuff 
            if percent_fadein < 1.0:
                return percent_fadein

            # Else this is fade out period

            # If it is during the slider hold period, then it's fully visible.
            # Otherwise, it's not visible anymore
            if hitobject.is_hitobject_type(Hitobject.SLIDER):
                if time > hitobject.end_time: return 0.0
                else:                         return 1.0
            else:
                if time > hitobject.time: return 0.0
                else:                     return 1.0



    @staticmethod
    def get_circle_overlap_percentage(beatmap, hitobject, time):
        pass


    @staticmethod
    def get_surrounding_hitobjects(beatmap, hitobjects):
        if len(hitobjects) < 1: return

        hitobject_before_first = beatmap.get_previous_hitobject(hitobjects[0])
        if hitobject_before_first: 
            try: yield hitobject_before_first
            except AttributeError: pass

        for hitobject in hitobjects:
            try: yield hitobject
            except AttributeError: pass

        hitobject_after_last = beatmap.get_next_hitobject(hitobjects[-1])
        if hitobject_after_last: 
            try: yield hitobject_after_last
            except AttributeError: pass


    @staticmethod
    def get_surrounding_aimpoints(beatmap, hitobjects):
        if len(hitobjects) < 1: return

        hitobject_before_first = beatmap.get_previous_hitobject(hitobjects[0])
        if hitobject_before_first: 
            try: yield hitobject_before_first.raw_data()[-1]
            except IndexError: pass

        for hitobject in hitobjects:
            for score_point in hitobject.raw_data():
                 yield score_point

        hitobject_after_last = beatmap.get_next_hitobject(hitobjects[-1])
        if hitobject_after_last:
            try: yield hitobject_after_last.raw_data()[0]
            except IndexError: pass


    @staticmethod
    def get_aimpoints_from_hitobjects(hitobjects):
        return [ (hitobject.get_aimpoints()[0], hitobject.time_to_pos(hitobject.get_aimpoints()[0])) for hitobject in hitobjects ]