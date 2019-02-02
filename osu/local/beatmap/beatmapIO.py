import codecs

from .beatmap_utility import BeatmapUtil
from ..hitobject.hitobject import Hitobject
from ..hitobject.sliderhitobject import SliderHitobject


class BeatmapIO():

    class Metadata():

        def __init__(self):
            self.beatmap_format = -1    # *.osu format
            self.artist         = ''
            self.title          = ''
            self.version        = ''    # difficulty name
            self.creator        = ''
            self.name           = ''    # Artist - Title (Creator) [Difficulty]
            self.beatmap_md5    = None  # generatedilepath:


    class TimingPoint():

        def __init__(self):
            self.offset        = None
            self.beat_interval = None
            self.inherited     = None
            self.meter         = None
            

    class Section():

        SECTION_NONE         = 0
        SECTION_GENERAL      = 1
        SECTION_EDITOR       = 2
        SECTION_METADATA     = 3
        SECTION_DIFFICULTY   = 4
        SECTION_EVENTS       = 5
        SECTION_TIMINGPOINTS = 6
        SECTION_COLOURS      = 7
        SECTION_HITOBJECTS   = 8


    def __init__(self, filepath=None):
        self.__is_valid = False
        self.metadata      = BeatmapIO.Metadata()
        self.timing_points = []
        self.hitobjects    = []

        self.section_map = {
            BeatmapIO.Section.SECTION_GENERAL      : self.__parse_general_section,
            BeatmapIO.Section.SECTION_EDITOR       : self.__parse_editor_section,
            BeatmapIO.Section.SECTION_METADATA     : self.__parse_metadata_section,
            BeatmapIO.Section.SECTION_DIFFICULTY   : self.__parse_difficulty_section,
            BeatmapIO.Section.SECTION_EVENTS       : self.__parse_events_section,
            BeatmapIO.Section.SECTION_TIMINGPOINTS : self.__parse_timingpoints_section,
            BeatmapIO.Section.SECTION_COLOURS      : self.__parse_colour_section,
            BeatmapIO.Section.SECTION_HITOBJECTS   : self.__parse_hitobjects_section
        }

        if filepath:
            self.load_beatmap(filepath)


    def load_beatmap(self, filepath):

        with open(filepath, 'rt', encoding='utf-8') as beatmap_file:
            self.__parse_beatmap_file(beatmap_file)
            self.__process()
            self.__validate()


    def save_beatmap(self, filepath):
        pass


    def get_md5(self):
        pass


    def get_copy(self):
        pass


    def get_hitobject_at_index(self, index):
        pass

    
    def get_hitobject_at_time(self, time):
        pass


    def get_timingpoint_at_index(self, index):
        pass

    
    def get_timingpoint_at_time(self, time):
        pass
        

    # Processes the beatmap after loading it
    def __process(self):
        pass


    # Validates beatmap data
    def __validate(self):
        pass


    def __parse_beatmap_file(self, beatmap_file):
        self.__parse_beatmap_file_format(beatmap_file)
        self.__parse_beatmap_file_data(beatmap_file)


    def __parse_beatmap_file_format(self, beatmap_file):
        line  = beatmap_file.readline()
        data  = line.split('osu file format v')
        
        try: self.metadata.beatmap_format = int(data[1])
        except: return


    def __parse_beatmap_file_data(self, beatmap_file):
        if self.metadata.beatmap_format == -1: return

        section = BeatmapIO.Section.SECTION_NONE
        line    = ''
        
        while True:
            line = beatmap_file.readline()

            if line.strip() == '[General]':        section = BeatmapIO.Section.SECTION_GENERAL
            elif line.strip() == '[Editor]':       section = BeatmapIO.Section.SECTION_EDITOR
            elif line.strip() == '[Metadata]':     section = BeatmapIO.Section.SECTION_METADATA
            elif line.strip() == '[Difficulty]':   section = BeatmapIO.Section.SECTION_DIFFICULTY
            elif line.strip() == '[Events]':       section = BeatmapIO.Section.SECTION_EVENTS
            elif line.strip() == '[TimingPoints]': section = BeatmapIO.Section.SECTION_TIMINGPOINTS
            elif line.strip() == '[Colours]':      section = BeatmapIO.Section.SECTION_COLOURS
            elif line.strip() == '[HitObjects]':   section = BeatmapIO.Section.SECTION_HITOBJECTS
            elif line == '':               
                return
            else:
                self.__parse_section(section, line)


    def __parse_section(self, section, line):
        if section != BeatmapIO.Section.SECTION_NONE:
            self.section_map[section](line)


    def __parse_general_section(self, line):
        data = line.split(':', 1)
        if len(data) < 2: return
        data[0] = data[0].strip()

        if data[0] == 'PreviewTime':
            # ignore
            return

        if data[0] == 'Countdown':
            # ignore
            return

        if data[0] == 'SampleSet':
            # ignore
            return

        if data[0] == 'StackLeniency':
            # ignore
            return

        if data[0] == 'Mode':
            self.gamemode = int(data[1])
            return

        if data[0] == 'LetterboxInBreaks':
            # ignore
            return

        if data[0] == 'SpecialStyle':
            # ignore
            return

        if data[0] == 'WidescreenStoryboard':
            # ignore
            return


    def __parse_editor_section(self, line):
        data = line.split(':', 1)
        if len(data) < 2: return

        if data[0] == 'DistanceSpacing':
            # ignore
            return

        if data[0] == 'BeatDivisor':
            # ignore
            return

        if data[0] == 'GridSize':
            # ignore
            return

        if data[0] == 'TimelineZoom':
            # ignore
            return



    def __parse_metadata_section(self, line):
        data = line.split(':', 1)
        if len(data) < 2: return
        data[0] = data[0].strip()

        if data[0] == 'Title':
            self.metadata.title = data[1].strip()
            return

        if data[0] == 'TitleUnicode':
            # ignore
            return

        if data[0] == 'Artist':
            self.metadata.artist = data[1].strip()
            return

        if data[0] == 'ArtistUnicode':
            # ignore
            return

        if data[0] == 'Creator':
            self.metadata.creator = data[1].strip()
            return

        if data[0] == 'Version':
            self.metadata.version = data[1].strip()
            return

        if data[0] == 'Source':
            # ignore
            return

        if data[0] == 'Tags':
            # ignore
            return

        if data[0] == 'BeatmapID':
            # ignore
            return

        if data[0] == 'BeatmapSetID':
            # ignore
            return


    def __parse_difficulty_section(self, line):
        data = line.split(':', 1)
        if len(data) < 2: return
        data[0] = data[0].strip()

        if data[0] == 'HPDrainRate':
            self.hp = float(data[1])
            return

        if data[0] == 'CircleSize':
            self.cs = float(data[1])
            return

        if data[0] == 'OverallDifficulty':
            self.od = float(data[1])
            return

        if data[0] == 'ApproachRate':
            self.ar = float(data[1])
            return

        if data[0] == 'SliderMultiplier':
            self.sm = float(data[1])
            return

        if data[0] == 'SliderTickRate':
            self.st = float(data[1])
            return


    def __parse_events_section(self, line):
        # ignore
        return


    def __parse_timingpoints_section(self, line):
        data = line.split(',')
        if len(data) < 2: return

        timing_point = BeatmapIO.TimingPoint()
        
        timing_point.offset        = int(data[0])
        timing_point.beat_interval = float(data[1])

        # Old maps don't have meteres
        if len(data) > 2: timing_point.meter = int(data[2])
        else:             timing_point.meter = 4

        if len(data) > 6: timing_point.inherited = False if int(data[6]) == 1 else True
        else:             timing_point.inherited = False

        self.timing_points.append(timing_point)


    def __parse_colour_section(self, line):
        # ignore
        return


    def __parse_hitobjects_section(self, line):
        data = line.split(',')
        if len(data) < 2: return
        
        self.hitobject_type = int(data[3])

        if BeatmapUtil.is_hitobject_type(self.hitobject_type, Hitobject.CIRCLE):
            self.hitobjects.append(Hitobject(data))
            return

        if BeatmapUtil.is_hitobject_type(self.hitobject_type, Hitobject.SLIDER):
            self.hitobjects.append(SliderHitobject(data))
            return

        if BeatmapUtil.is_hitobject_type(self.hitobject_type, Hitobject.SPINNER):
            self.hitobjects.append(Hitobject(data))
            return

        if BeatmapUtil.is_hitobject_type(self.hitobject_type, Hitobject.MANIALONG):
            self.hitobjects.append(SliderHitobject(data))
            return


    def __process_timing_points(self):
        pass
    

    def __process_slider_data(self):
        pass