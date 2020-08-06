import unittest

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.replay.replayIO import ReplayIO

from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.replay_data import StdReplayData
from analysis.osu.std.score_data import StdScoreData



class TestStdScoreData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\test\\abraker - unknown (abraker) [250ms].osu')


    @classmethod
    def tearDown(cls):  
        pass


    def test_get_score_data(self):
        # TODO
        pass


    def test_get_velocity_jump_frames(self):
        # TODO
        pass


    def test_tap_offset_mean(self):
        # TODO
        pass


    def test_tap_offset_var(self):
        # TODO
        pass


    def test_tap_offset_stdev(self):
        # TODO
        pass


    def test_cursor_pos_offset_mean(self):
        # TODO
        pass


    def test_cursor_pos_offset_var(self):
        # TODO
        pass


    def test_cursor_pos_offset_stdev(self):
        # TODO
        pass


    def test_odds_some_tap_within(self):
        # TODO
        pass


    def test_odds_some_cursor_within(self):
        # TODO
        pass


    def test_odds_all_tap_within(self):
        # TODO
        pass


    def test_odds_all_cursor_within(self):
        # TODO
        pass


    def test_odds_all_conditions_within(self):
        # TODO
        pass