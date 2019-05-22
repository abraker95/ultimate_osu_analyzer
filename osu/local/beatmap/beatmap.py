from PyQt5.QtCore import QObject, pyqtSignal
from misc.callback import callback
from misc.frozen_cls import FrozenCls

from osu.local.hitobject.std.std import Std
from osu.local.hitobject.mania.mania import Mania

'''
Description: Provides a manupilation interface for beatmaps

Input: 
    load_beatmap - load the beatmap specified

Output:
    hitobjects - list of hitobjects present in the map
    timingpoints - list of timing points present in the map
'''
@FrozenCls
class Beatmap():

    GAMEMODE_OSU   = 0
    GAMEMODE_TAIKO = 1
    GAMEMODE_CATCH = 2
    GAMEMODE_MANIA = 3

    '''
    cs_changed        = pyqtSignal(float)
    ar_changed        = pyqtSignal()
    od_changed        = pyqtSignal()
    timings_changed   = pyqtSignal()
    positions_changed = pyqtSignal()
    '''

    @FrozenCls
    class Metadata():

        def __init__(self):
            self.beatmap_format = -1    # *.osu format
            self.artist         = ''
            self.title          = ''
            self.version        = ''    # difficulty name
            self.creator        = ''
            self.name           = ''    # Artist - Title (Creator) [Difficulty]
            
            self.beatmap_id     = None
            self.beatmapset_id  = None
            self.beatmap_md5    = None  # generatedilepath:

    
    @FrozenCls
    class TimingPoint():

        def __init__(self):
            self.offset        = None
            self.beat_interval = None
            self.inherited     = None
            self.meter         = None

            self.beat_length       = None
            self.bpm               = None
            self.slider_multiplier = None


    @FrozenCls
    class Difficulty():

        def __init__(self):
            self.hp = None
            self.cs = None
            self.od = None
            self.ar = None
            self.sm = None
            self.st = None


    def __init__(self):
        self.metadata   = Beatmap.Metadata()
        self.difficulty = Beatmap.Difficulty()
        self.gamemode   = None
        
        self.timing_points     = []
        self.hitobjects        = []
        self.end_times         = []
        self.slider_tick_times = []

        self.bpm_min = float('inf')
        self.bpm_max = float('-inf')


    def get_time_range(self):
        print('get_time_range')
        if self.gamemode == Beatmap.GAMEMODE_OSU:   return Std.get_time_range(self.hitobjects)
        if self.gamemode == Beatmap.GAMEMODE_TAIKO: print('TODO: Taiko') #  return Taiko.get_time_range(self.hitobjects)
        if self.gamemode == Beatmap.GAMEMODE_CATCH: print('TODO: Catch') #  return Catch.get_time_range(self.hitobjects)
        if self.gamemode == Beatmap.GAMEMODE_MANIA: return Mania.get_time_range(self.hitobjects)


    """
    Returns:
        The number of hitobjects the beatmap has
    """
    def get_num_hitobjects(self):
        return len(self.hitobjects)


    """
    Args:
        index: (int) index of the hitobject to get
    
    Returns:
        The hitobject at the specified index
    """
    def get_hitobject_at_index(self, index):
        return self.hitobjects[index]

    
    """
    Searches for the earliest hitobject that is closest to the time specified.

    Args:
        time: (int/float) time of the closest hitobject to get
        end_time: (bool) whether to search the hitobject by its ending time or starting time
    
    Returns:
        The hitobject found at the specified time
    """
    def get_hitobject_at_time(self, time, end_time=False):
        if end_time:
            index = find(self.end_times.values(), time)
            return self.hitobjects[self.end_times[index]] if index != -1 else None
        else:
            index = find(self.hitobjects, time, lambda hitobject: hitobject.time)
            return self.hitobjects[index] if index != -1 else None


    def get_previous_hitobject(self, hitobject):
        idx = self.hitobjects.index(hitobject)
        if idx < 1: return None

        return self.hitobjects[idx - 1]


    def get_next_hitobject(self, hitobject):
        idx = self.hitobjects.index(hitobject)
        if idx > len(self.hitobjects) - 2: return None

        return self.hitobjects[idx + 1]

    
    def get_aimpoints(self, hitobjects):
        aimpoints = []
        for hitobject in hitobjects:
            try:
                for aimpoint in hitobject.get_aimpoints():
                    aimpoints.append( (aimpoint, hitobject.time_to_pos(aimpoint)) )
            except AttributeError: pass

        return sorted(aimpoints, key=lambda aimpoint: aimpoint[0])



    """
    Searches for the earliest timingpoint that is closest to the time specified.

    Args:
        time: (int/float) time of the closest timingpoint to get
    
    Returns:
        The timingpoint found at the specified time
    """
    def get_timingpoint_at_time(self, time):
        pass

    
    def set_rate_mult(self, rate):
        # TODO
        self.timings_changed.emit()


    def set_rate_bpm(self, rate):
        # TODO
        self.timings_changed.emit()


    def get_rate_mult(self):
        pass


    def get_rate_bpm(self):
        pass


    def rotate_beatmap(self, radians):
        # TODO
        self.positions_changed.emit()


    def flip_beatmap(self, axis_radians):
        # TODO
        self.positions_changed.emit()


    def set_cs_val(self, cs):
        self.difficulty.cs = cs

    
    def set_cs_px(self, px):
        self.difficulty.cs = Osu.px_to_cs(px)


    def get_cs_val(self):
        return self.cs


    def get_cs_px(self):
        return Osu.cs_to_px(self.difficulty.cs)


    def set_ar_val(self, ar):
        self.difficulty.ar = ar
        #self.ar_changed.emit()


    def set_ar_ms(self, ms):
        self.difficulty.ar = Osu.ms_to_ar(ms)
        #self.ar_changed.emit()


    def get_ar_val(self):
        return self.difficulty.ar


    def get_ar_ms(self):
        return Osu.ar_to_ms(self.difficulty.ar)


    def set_od_val(self, od):
        self.difficulty.od = od
        #self.od_changed.emit()


    def get_od_val(self):
        return self.difficulty.od


    def apply_mods(self, mods):
        # TODO: return modified beatmap
        pass