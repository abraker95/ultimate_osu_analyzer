


class BeatmapUtil():

    PLAYFIELD_WIDTH  = 640
    PLAYFIELD_HEIGHT = 480

    @staticmethod
    def cs_to_px(cs):
        return 109 - 9*cs


    @staticmethod
    def px_to_cs(px):
        return (109 - px)/9


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
        return 79.5 - 6.0*od


    @staticmethod
    def ms_to_od300(ms):
        return (79.5 - ms)/6.0


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
    def get_num_hitobjects_visible_at_index(beatmap, index):
        pass


    @staticmethod
    def get_num_hitobjects_visible_at_time(beatmap, time):
        pass


    @staticmethod
    def is_visible_at(beatmap, hitobject, time):
        pass


    @staticmethod
    def get_opacity_at(beatmap, hitobject, time):
        pass


    @staticmethod
    def get_circle_overlap_percentage(beatmap, hitobject, time):
        pass