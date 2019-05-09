from PyQt5.QtCore import QObject, pyqtSignal
from .beatmap_utility import BeatmapUtil
from misc.callback import callback
from misc.frozen_cls import FrozenCls


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


    def __init__(self):
        #QObject.__init__(self)
        #BeatmapIO.__init__(self, filepath)

        self.metadata = Beatmap.Metadata()
        self.gamemode = None
        
        self.timing_points     = []
        self.hitobjects        = []
        self.end_times         = []
        self.slider_tick_times = []

        self.hp = None
        self.cs = None
        self.od = None
        self.ar = None
        self.sm = None
        self.st = None

        #self.slider_tick_times = []
        self.bpm_min = float('inf')
        self.bpm_max = float('-inf')


    def get_time_range(self):
        return (self.hitobjects[0].time, list(self.end_times.keys())[-1])


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


    @callback
    def set_cs_val(self, cs):
        self.cs = cs
        self.set_cs_val.emit(BeatmapUtil.cs_to_px(cs))

    
    def set_cs_px(self, px):
        self.cs = BeatmapUtil.px_to_cs(px)
        self.cs_changed.emit(px)


    def get_cs_val(self):
        return self.cs


    def get_cs_px(self):
        return BeatmapUtil.cs_to_px(self.cs)


    def set_ar_val(self, ar):
        self.ar = ar
        self.ar_changed.emit()


    def set_ar_ms(self, ms):
        self.ar = BeatmapUtil.ms_to_ar(ms)
        self.ar_changed.emit()


    def get_ar_val(self):
        return self.ar


    def get_ar_ms(self):
        return BeatmapUtil.ar_to_ms(self.ar)


    def set_od_val(self, od):
        self.od = od
        self.od_changed.emit()


    def get_od_val(self):
        return self.od


    def apply_mods(self, mods):
        # TODO: return modified beatmap
        pass