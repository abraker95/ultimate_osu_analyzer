from misc.math_utils import *
from ..hitobject.hitobject import Hitobject



"""
Provides utilities for beatmap and hitobject related calculation
"""
class BeatmapUtil():

    PLAYFIELD_WIDTH  = 512
    PLAYFIELD_HEIGHT = 384

    @staticmethod
    def cs_to_px(cs):
        return (109 - 9*cs)/2


    @staticmethod
    def px_to_cs(px):
        return 2*(109 - px)/9


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
        return 4*BeatmapUtil.cs_to_px(cs) - 3*BeatmapUtil.cs_to_px(cs) * (t/max(800, BeatmapUtil.ar_to_ms(ar)))


    @staticmethod
    def is_hitobject_type(hitobject_type, compare):
        return hitobject_type & compare > 0


    @staticmethod
    def get_fadein_period(ar_ms, hidden_mod=False):
        if hidden_mod:
            return 0.4 * ar_ms
        else:
            return min(ar_ms, 400)


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

        idx_begin_time_latest = find(beatmap.hitobjects, time, lambda hitobject: hitobject.time - BeatmapUtil.ar_to_ms(beatmap.ar))
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
    def get_aimpoints_from_hitobjects(beatmap, hitobjects):
        if len(hitobjects) < 1: return

        hitobject_before_first = beatmap.get_previous_hitobject(hitobjects[0])
        if hitobject_before_first: 
            try:
                time = hitobject_before_first.get_aimpoints()[-1]
                yield (time, hitobject_before_first.time_to_pos(time))
            except AttributeError: pass

        for hitobject in hitobjects:
            try: 
                for aimpoint in hitobject.get_aimpoints():
                    time = aimpoint
                    yield (time, hitobject.time_to_pos(time))
            except AttributeError: pass

        hitobject_after_last = beatmap.get_next_hitobject(hitobjects[-1])
        if hitobject_after_last: 
            try:
                time = hitobject_after_last.get_aimpoints()[0]
                yield (time, hitobject_after_last.time_to_pos(time))
            except AttributeError: pass 