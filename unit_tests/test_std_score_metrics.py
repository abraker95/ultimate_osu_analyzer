import unittest

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.replay.replayIO import ReplayIO

from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.replay_data import StdReplayData
from analysis.osu.std.score_data import StdScoreData
from analysis.osu.std.score_metrics import StdScoreMetrics



class TestStdScoreMetrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\test\\abraker - unknown (abraker) [250ms].osu')


    @classmethod
    def tearDown(cls):  
        pass


    def test_get_per_hitobject_score_data(self):
        # TODO
        pass


    def test_get_percent_below_offset_one(self):
        # TODO
        pass


    def test_percent_players_taps_all(self):
        # TODO
        pass


    def test_solve_for_hit_offset_one(self):
        # TODO
        pass


    def test_solve_for_hit_offset_all(self):
        # TODO
        pass