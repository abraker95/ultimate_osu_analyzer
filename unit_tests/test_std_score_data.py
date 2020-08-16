import unittest

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.replay.replayIO import ReplayIO

from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.replay_data import StdReplayData
from analysis.osu.std.score_data import StdScoreData



class TestStdScoreData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\test\\score_test.osu')
        cls.map_data = StdMapData.get_map_data(beatmap.hitobjects)


    @classmethod
    def tearDown(cls):  
        pass


    def test_get_key_state(self):
        # Shorthand
        FREE = StdReplayData.FREE
        PRESS = StdReplayData.PRESS
        HOLD = StdReplayData.HOLD
        RELEASE = StdReplayData.RELEASE

        # free -> all free
        key_state = StdScoreData._StdScoreData__get_key_state(FREE, [ FREE, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, FREE)

        # TODO: this is an illegal state (you can't have a press transition into a free, it must go to a release first)
        #key_state = StdScoreData._StdScoreData__get_key_state(PRESS, [ FREE, FREE, FREE, FREE ], press_block=False, release_block=False)
        #self.assertEqual(key_state, )

        # TODO: this is an illegal state (you can't have a hold transition into a free, it must go to a release first)
        #key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ FREE, FREE, FREE, FREE ], press_block=False, release_block=False)
        #self.assertEqual(key_state, )

        # release -> all free
        key_state = StdScoreData._StdScoreData__get_key_state(RELEASE, [ FREE, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, FREE)

        # free -> one press
        key_state = StdScoreData._StdScoreData__get_key_state(FREE, [ PRESS, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # press -> one press
        key_state = StdScoreData._StdScoreData__get_key_state(PRESS, [ PRESS, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # hold -> one press (non blocking)
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ PRESS, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # hold -> one press (blocking)
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ PRESS, FREE, FREE, FREE ], press_block=True, release_block=False)
        self.assertEqual(key_state, HOLD)

        # TODO: this is an illegal state (you can't have a release transition into a press, it must go to a free first)
        #key_state = StdScoreData._StdScoreData__get_key_state(RELEASE, [ PRESS, FREE, FREE, FREE ], press_block=False, release_block=False)
        #self.assertEqual(key_state, )

        # TODO: this is an illegal state (you can't have a free transition into a hold, it must go to a press first)
        #key_state = StdScoreData._StdScoreData__get_key_state(FREE, [ HOLD, FREE, FREE, FREE ], press_block=False, release_block=False)
        #self.assertEqual(key_state, )

        # press -> one hold
        key_state = StdScoreData._StdScoreData__get_key_state(PRESS, [ HOLD, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, HOLD)

        # hold -> one hold
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ HOLD, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, HOLD)

        # TODO: this is an illegal state (you can't have a release transition into a hold, it must go to press first)
        #key_state = StdScoreData._StdScoreData__get_key_state(RELEASE, [ HOLD, FREE, FREE, FREE ], press_block=False, release_block=False)
        #self.assertEqual(key_state, )

        # press -> one release
        key_state = StdScoreData._StdScoreData__get_key_state(PRESS, [ RELEASE, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, RELEASE)

        # Test hold -> one release (non blocking)
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ RELEASE, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, RELEASE)

        # hold -> one release (blocking)      
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ RELEASE, FREE, FREE, FREE ], press_block=False, release_block=True)
        self.assertEqual(key_state, HOLD)

        # release -> one release
        key_state = StdScoreData._StdScoreData__get_key_state(RELEASE, [ RELEASE, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, RELEASE)

        # free -> one press, one release
        key_state = StdScoreData._StdScoreData__get_key_state(FREE, [ PRESS, RELEASE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # press -> one press, one release
        key_state = StdScoreData._StdScoreData__get_key_state(FREE, [ PRESS, RELEASE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # hold -> one press, one release (non blocking)
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ PRESS, RELEASE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # hold -> one press, one release (press blocking)
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ PRESS, RELEASE, FREE, FREE ], press_block=True, release_block=False)
        self.assertEqual(key_state, RELEASE)

        # hold -> one press, one release (release blocking)
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ PRESS, RELEASE, FREE, FREE ], press_block=False, release_block=True)
        self.assertEqual(key_state, PRESS)

        # hold -> one press, one release (press blocking, release blocking)
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ PRESS, RELEASE, FREE, FREE ], press_block=True, release_block=True)
        self.assertEqual(key_state, HOLD)

        # hold -> one hold, one release (non blocking)        
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ HOLD, RELEASE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, RELEASE)

        # hold -> one hold, one release (blocking)
        key_state = StdScoreData._StdScoreData__get_key_state(HOLD, [ HOLD, RELEASE, FREE, FREE ], press_block=False, release_block=True)
        self.assertEqual(key_state, HOLD)


    def test_get_score_data(self):
        # TODO: This replay has cursor pressing and wander in random parts sometimes making a hit
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - aim_miss [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        #self.assertTrue(all(score_data['type'] == StdScoreData.TYPE_MISS))

        # This replay has no hits made, making all notes miss
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - no_press [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        self.assertTrue(all(score_data['type'] == StdScoreData.TYPE_MISS))

        # This replay has mouse buttons are pressed at same time for every hit. Each hit is successful
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - both_keys_mouse_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))

        # This replay has both keys are pressed at same time for every hit. Each hit is successful
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - both_keys_tap [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))

        # This replay has the player double tapping every note, creating an extra tap after the note has been hit
        # The player also randomly taps through out the slider
        # TODO: Test recoverable release option being false for this replay
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - double_tap [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        #self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))

        # In this replay the taps are early
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - early_press [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))

        # TODO: In this replay the first note is missed
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - first_note_miss [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        #self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))

        # TODO: In this replay the last note is missed
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - last_note_miss [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        #self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))

        # TODO: In this replay a note in the middle is missed
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - mid_note_miss [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        #self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))

        # TODO: In this replay notes are randomly missed
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - random_miss [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        #self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))

        # TODO: Keys are randomly pressed
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - rapid_press [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        #self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))

        # The map is SS'd in this replay
        replay = ReplayIO.open_replay('unit_tests/replays/osu/abraker - ss_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))

        # osu! autoplay
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        self.assertTrue(not any(score_data['type'] == StdScoreData.TYPE_MISS))


    def test_tap_press_offsets(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        tap_press_offsets = StdScoreData.tap_press_offsets(score_data)
        self.assertTrue(all(tap_press_offsets == 0))


    def test_release_offsets(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        tap_release_offsets = StdScoreData.tap_release_offsets(score_data)
        self.assertTrue(all(tap_release_offsets == 0))



    def test_aim_x_offsets(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        aim_x_offsets = StdScoreData.aim_x_offsets(score_data)
        self.assertTrue(all(aim_x_offsets == 0))


    def test_aim_y_offsets(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        aim_y_offsets = StdScoreData.aim_y_offsets(score_data)
        self.assertTrue(all(aim_y_offsets == 0))


    def test_aim_offsets(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        aim_offsets = StdScoreData.aim_offsets(score_data)
        self.assertTrue(all(aim_offsets == 0))


    def test_tap_offset_mean(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        tap_offset_mean = StdScoreData.tap_offset_mean(score_data)
        self.assertEqual(tap_offset_mean, 0)


    def test_tap_offset_var(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        tap_offset_var = StdScoreData.tap_offset_var(score_data)
        self.assertEqual(tap_offset_var, 0)


    def test_tap_offset_stdev(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        tap_offset_stdev = StdScoreData.tap_offset_stdev(score_data)
        self.assertEqual(tap_offset_stdev, 0)


    def test_cursor_pos_offset_mean(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        cursor_pos_offset_mean = StdScoreData.cursor_pos_offset_mean(score_data)
        self.assertEqual(cursor_pos_offset_mean, 0)


    def test_cursor_pos_offset_var(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        cursor_pos_offset_var = StdScoreData.cursor_pos_offset_var(score_data)
        self.assertEqual(cursor_pos_offset_var, 0)


    def test_cursor_pos_offset_stdev(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        cursor_pos_offset_stdev = StdScoreData.cursor_pos_offset_stdev(score_data)
        self.assertEqual(cursor_pos_offset_stdev, 0)


    def test_odds_some_tap_within(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        odds_some_tap_within = StdScoreData.odds_some_tap_within(score_data, 1)
        self.assertEqual(odds_some_tap_within, 1.0)


    def test_odds_some_cursor_within(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        odds_some_tap_within = StdScoreData.odds_some_cursor_within(score_data, 1)
        self.assertEqual(odds_some_tap_within, 1.0)


    def test_odds_all_tap_within(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        odds_all_tap_within = StdScoreData.odds_all_tap_within(score_data, 1)
        self.assertEqual(odds_all_tap_within, 1.0)


    def test_odds_all_cursor_within(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        odds_all_cursor_within = StdScoreData.odds_all_cursor_within(score_data, 1)
        self.assertEqual(odds_all_cursor_within, 1.0)


    def test_odds_all_conditions_within(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, self.map_data)

        odds_all_conditions_within = StdScoreData.odds_all_conditions_within(score_data, 1, 1)
        self.assertEqual(odds_all_conditions_within, 1.0)