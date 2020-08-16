import unittest

from osu.local.beatmap.beatmapIO import BeatmapIO
from analysis.osu.std.map_data import StdMapData



class TestStdMapData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\test\\abraker - unknown (abraker) [250ms].osu')


    @classmethod
    def tearDown(cls):  
        pass


    def test_std_hitobject_to_aimpoints(self):
        for hitobject in self.beatmap.hitobjects:
            aimpoint_data = StdMapData.std_hitobject_to_aimpoints(hitobject)


    def test_get_map_data(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)


    def test_get_num_hitobjects(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        num_hitobjects = StdMapData.get_num_hitobjects(map_data)


    def test_get_presses(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        presses = StdMapData.get_presses(map_data)


    def test_get_data_before(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        map_data = StdMapData.get_data_before(map_data, 1000)


    def test_get_data_after(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        map_data = StdMapData.get_data_after(map_data, 1000)


    def test_time_slice(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        map_data = StdMapData.time_slice(map_data, 1000, 2000, True)


    def test_start_times(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        start_times = StdMapData.start_times(map_data)


    def test_end_times(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        end_times = StdMapData.end_times(map_data)