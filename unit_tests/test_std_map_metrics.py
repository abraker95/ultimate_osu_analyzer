import unittest

from osu.local.beatmap.beatmapIO import BeatmapIO

from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.map_metrics import StdMapMetrics



class TestStdMapMetrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\test\\abraker - unknown (abraker) [250ms].osu')
        cls.map_data = StdMapData.get_map_data(cls.beatmap.hitobjects)


    @classmethod
    def tearDown(cls):  
        pass


    def test_calc_tapping_intervals(self):
        tapping_intervals = StdMapMetrics.calc_tapping_intervals(self.map_data)


    def test_calc_notes_per_sec(self):
        tapping_intervals = StdMapMetrics.calc_notes_per_sec(self.map_data)


    def test_calc_path_dist(self):
        path_dist = StdMapMetrics.calc_path_dist(self.map_data)


    def test_calc_path_vel(self):
        path_vel = StdMapMetrics.calc_path_vel(self.map_data)


    def test_calc_path_accel(self):
        path_accel = StdMapMetrics.calc_path_accel(self.map_data)


    def test_calc_xy_dist(self):
        xy_dist = StdMapMetrics.calc_xy_dist(self.map_data)


    def test_calc_xy_vel(self):
        xy_vel = StdMapMetrics.calc_xy_vel(self.map_data)


    def test_calc_xy_accel(self):
        xy_accel = StdMapMetrics.calc_xy_accel(self.map_data)


    def test_calc_xy_jerk(self):
        xy_accel = StdMapMetrics.calc_xy_accel(self.map_data)


    def test_calc_angles(self):
        angles = StdMapMetrics.calc_angles(self.map_data)


    def test_calc_theta_per_second(self):
        theta_per_sec = StdMapMetrics.calc_theta_per_second(self.map_data)


    def test_calc_radial_velocity(self):
        radial_vel = StdMapMetrics.calc_radial_velocity(self.map_data)


    def test_calc_perp_int(self):
        perp_int = StdMapMetrics.calc_perp_int(self.map_data)


    def test_calc_lin_int(self):
        lin_int = StdMapMetrics.calc_lin_int(self.map_data)