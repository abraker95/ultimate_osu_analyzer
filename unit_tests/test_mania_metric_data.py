import unittest

from osu.local.beatmap.beatmapIO import BeatmapIO
from analysis.osu.mania.action_data import ManiaActionData
from analysis.osu.mania.map_metrics import ManiaMapMetrics



class TestManiaMetricData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDown(cls):  
        pass


    def test_calc_press_rate(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        press_rate = ManiaMapMetrics.calc_press_rate(action_data)


    def test_calc_note_intervals(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        note_intervals = ManiaMapMetrics.calc_note_intervals(action_data, 0)


    def test_max_press_rate_per_col(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        press_rate = ManiaMapMetrics.calc_max_press_rate_per_col(action_data)


    def test_detect_single_note_releases(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        mask = ManiaMapMetrics.detect_presses_during_holds(action_data)


    def test_detect_presses_during_holds(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        mask = ManiaMapMetrics.detect_presses_during_holds(action_data)


    def test_detect_holds_during_release(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        mask = ManiaMapMetrics.detect_holds_during_release(action_data)


    def test_detect_hold_notes(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        mask = ManiaMapMetrics.detect_hold_notes(action_data)


    def test_data_to_press_durations(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        press_intervals = ManiaMapMetrics.data_to_press_durations(action_data)


    def test_data_to_hold_durations(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        hold_note_durations = ManiaMapMetrics.data_to_hold_durations(action_data)


    def test_data_to_anti_press_durations(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        anti_press_durations = ManiaMapMetrics.data_to_anti_press_durations(action_data)


    def test_detect_inverse(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        inverse_mask = ManiaMapMetrics.detect_inverse(action_data)


    def test_detect_chords(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        chord_mask = ManiaMapMetrics.detect_chords(action_data)


    def test_detect_jacks(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        jack_mask = ManiaMapMetrics.detect_jacks(action_data)


    '''
    def test_calc_notes_per_sec(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        notes_per_sec = ManiaMapMetrics.calc_notes_per_sec(action_data)


    def test_calc_avg_nps_col(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        avg_nps_col = ManiaMapMetrics.calc_avg_nps_col(action_data)


    def test_calc_avg_nps(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\chords_250ms.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        avg_nps = ManiaMapMetrics.calc_avg_nps(action_data)
    '''