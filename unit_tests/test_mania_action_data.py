import unittest

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.replay.replayIO import ReplayIO
from analysis.osu.mania.action_data import ManiaActionData



class TestManiaActionData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDown(cls):  
        pass


    def test_get_map_data_crash(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\1k_10x_0.25_chords.osu')
        ManiaActionData.get_map_data(beatmap.hitobjects)

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\2k_10x_0.25_chords.osu')
        ManiaActionData.get_map_data(beatmap.hitobjects)

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\3k_10x_0.25_chords.osu')
        ManiaActionData.get_map_data(beatmap.hitobjects)

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\4k_10x_0.25_chords.osu')
        ManiaActionData.get_map_data(beatmap.hitobjects)

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\5k_10x_0.25_chords.osu')
        ManiaActionData.get_map_data(beatmap.hitobjects)

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\7k_10x_0.25_chords.osu')
        ManiaActionData.get_map_data(beatmap.hitobjects)

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\8k_mixed_timing_jacks.osu')
        ManiaActionData.get_map_data(beatmap.hitobjects)

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\14k_test.osu')
        ManiaActionData.get_map_data(beatmap.hitobjects)

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\18k_test.osu')
        ManiaActionData.get_map_data(beatmap.hitobjects)


    def test_get_replay_data_crash(self):
        replay = ReplayIO.open_replay('unit_tests\\replays\\mania\\osu!topus! - DJ Genericname - Dear You [S.Star\'s 4K HD+] (2019-05-29) OsuMania.osr')
        ManiaActionData.get_replay_data(replay.play_data, 4)


    def test_single_note_min_press_duration(self):
        # This map has all single notes
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\1k_10x_0.25_chords.osu')

        def test_press_duration(min_press_duration):
            # Even though single notes technically should begin and end on same timing,
            # the way action_data works requires that all notes start and end times be different.
            # Data in the array cannot have two same timings for multiple things since timings are saved as indexes
            action_data = ManiaActionData.get_map_data(beatmap.hitobjects, min_press_duration=min_press_duration)

            # Get note press and release timings
            end_times   = action_data[action_data[0] == ManiaActionData.RELEASE]
            start_times = action_data[action_data[0] == ManiaActionData.PRESS]

            # Subtract all timings where notes end by timings where notes start
            press_durations = end_times.index - start_times.index
            self.assertTrue((min_press_duration == press_durations).all(), f'Not all press durations are {min_press_duration} ms')

        for i in range(1, 100, 20):
            test_press_duration(i)


    def test_num_keys(self):
        def test_keys(keys):
            beatmap = BeatmapIO.open_beatmap(f'unit_tests\\maps\\mania\\test\\{keys}k_10x_0.25_chords.osu')
            action_data = ManiaActionData.get_map_data(beatmap.hitobjects)
            self.assertEqual(ManiaActionData.num_keys(action_data), keys, 'Calculated wrong number of keys')

        for key in [ 1, 2, 3, 4, 5, 6, 7 ]: 
            test_keys(key)


    def test_press_times(self):
        # This map has notes every 250ms
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\1k_10x_0.25_chords.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # Notes occur every 500 ms
        press_times = ManiaActionData.press_times(action_data, 0)
        for timing, i in zip(press_times, range(0, 500*10, 500)):
            self.assertEqual(timing, i, 'Timings do not match')


    def test_release_times(self):
        # This map has notes every 250ms
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\1k_10x_0.25_chords.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # Notes occur every 500 ms + 1 ms for release
        release_times = ManiaActionData.release_times(action_data, 0)
        for timing, i in zip(release_times, range(0, 500*10, 500)):
            self.assertEqual(timing, i + 1, 'Timings do not match')


    def test_filter_free(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\8k_mixed_timing_jacks.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        ManiaActionData.filter_free(action_data)


    def test_fill_holds(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\8k_mixed_timing_jacks.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        ManiaActionData.fill_holds(action_data)


    def test_split_by_hand(self):
        def test_keys(keys, lh, rh):
            beatmap = BeatmapIO.open_beatmap(f'unit_tests\\maps\\mania\\test\\{keys}k_10x_0.25_chords.osu')
            action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

            left_hand, right_hand = ManiaActionData.split_by_hand(action_data, left_handed=True)
            self.assertEqual(ManiaActionData.num_keys(left_hand),  lh, 'Left hand has wrong number of keys')
            self.assertEqual(ManiaActionData.num_keys(right_hand), rh, 'Right hand has wrong number of keys')

            lh, rh = rh, lh
            left_hand, right_hand = ManiaActionData.split_by_hand(action_data, left_handed=False)
            self.assertEqual(ManiaActionData.num_keys(left_hand),  lh, 'Left hand has wrong number of keys')
            self.assertEqual(ManiaActionData.num_keys(right_hand), rh, 'Right hand has wrong number of keys')

        test_keys(1, 1, 0)
        test_keys(2, 1, 1)
        test_keys(3, 2, 1)
        test_keys(4, 2, 2)
        test_keys(5, 3, 2)
        test_keys(6, 3, 3)
        test_keys(7, 4, 3)


    def test_mask_actions(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\8k_mixed_timing_jacks.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        ManiaActionData.mask_actions(action_data, ManiaActionData.FREE)
        ManiaActionData.mask_actions(action_data, ManiaActionData.PRESS)
        ManiaActionData.mask_actions(action_data, ManiaActionData.RELEASE)
        ManiaActionData.mask_actions(action_data, ManiaActionData.HOLD)


    def test_count_actions(self):
        def test_keys(keys):
            beatmap = BeatmapIO.open_beatmap(f'unit_tests\\maps\\mania\\test\\{keys}k_10x_0.25_chords.osu')
            action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

            # Each of the nk_10x_0.25_chords maps have a known amount of notes (n keys x 10 notes)
            self.assertEqual(ManiaActionData.count_actions(action_data, ManiaActionData.PRESS), keys * 10, 'Calculated wrong number of presses')
            self.assertEqual(ManiaActionData.count_actions(action_data, ManiaActionData.RELEASE), keys * 10, 'Calculated wrong number of releases')

        for key in [ 1, 2, 3, 4, 5, 6, 7 ]: 
            test_keys(key)

        # TODO: Test FREE and HOLD functionality


    def test_get_actions_between(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\8k_mixed_timing_jacks.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        ManiaActionData.get_actions_between(action_data, 0, 100)


    def test_is_action_in(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\8k_mixed_timing_jacks.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        ManiaActionData.is_action_in(action_data, ManiaActionData.PRESS, 0)


    def test_idx_next_action(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\test\\8k_mixed_timing_jacks.osu')
        action_data = ManiaActionData.get_map_data(beatmap.hitobjects)

        # TODO: test functionality
        ManiaActionData.idx_next_action(action_data, 0, ManiaActionData.PRESS)