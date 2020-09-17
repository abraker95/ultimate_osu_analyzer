import unittest
import pandas as pd

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.replay.replayIO import ReplayIO

from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.replay_data import StdReplayData
from analysis.osu.std.score_data import StdScoreData



class TestStdScoreData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\test\\score_test.osu')
        
        map_data = [ 
            pd.DataFrame(
            [
                [ 100, 0,   0, StdMapData.TYPE_PRESS, StdMapData.TYPE_SLIDER ],
                [ 350, 100, 0, StdMapData.TYPE_HOLD, StdMapData.TYPE_SLIDER ],
                [ 600, 200, 0, StdMapData.TYPE_HOLD, StdMapData.TYPE_SLIDER ],
                [ 750, 300, 0, StdMapData.TYPE_RELEASE, StdMapData.TYPE_SLIDER ],
            ],
            columns=['time', 'x', 'y', 'type', 'object']),
            pd.DataFrame(
            [ 
                [ 1000, 500, 500, StdMapData.TYPE_PRESS, StdMapData.TYPE_CIRCLE ],
                [ 1001, 500, 500, StdMapData.TYPE_RELEASE, StdMapData.TYPE_CIRCLE ],
            ],
            columns=['time', 'x', 'y', 'type', 'object']),
            pd.DataFrame(
            [ 
                [ 2000, 300, 300, StdMapData.TYPE_PRESS, StdMapData.TYPE_CIRCLE ],
                [ 2001, 300, 300, StdMapData.TYPE_RELEASE, StdMapData.TYPE_CIRCLE ],
            ],
            columns=['time', 'x', 'y', 'type', 'object']),
        ]
        cls.map_data = pd.concat(map_data, axis=0, keys=range(len(map_data)), names=[ 'hitobject', 'aimpoint' ])


    @classmethod
    def tearDown(cls):  
        pass


    def test_adv(self):
        map_time = 0

        # Time:        Before start
        # Hitobject:   Slider
        # Advancement: No operation
        adv = StdScoreData._StdScoreData__ADV_NOP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 0)

        # Time:        Before start
        # Hitobject:   Slider 
        # Advancement: Aimpoint
        adv = StdScoreData._StdScoreData__ADV_AIMP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 100)

        # Time:        Before start
        # Hitobject:   Slider
        # Advancement: Note
        adv = StdScoreData._StdScoreData__ADV_NOTE
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 100)

        map_time = 100

        # Time:        At first aimpoint
        # Hitobject:   Slider
        # Advancement: No operation
        adv = StdScoreData._StdScoreData__ADV_NOP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 100)

        # Time:        At first aimpoint
        # Hitobject:   Slider 
        # Advancement: Aimpoint
        adv = StdScoreData._StdScoreData__ADV_AIMP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 350)

        # Time:        At first aimpoint
        # Hitobject:   Slider
        # Advancement: Note
        adv = StdScoreData._StdScoreData__ADV_NOTE
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 1000)

        map_time = 350

        # Time:        At second aimpoint
        # Hitobject:   Slider
        # Advancement: No operation
        adv = StdScoreData._StdScoreData__ADV_NOP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 350)

        # Time:        At second aimpoint
        # Hitobject:   Slider 
        # Advancement: Aimpoint
        adv = StdScoreData._StdScoreData__ADV_AIMP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 600)

        # Time:        At second aimpoint
        # Hitobject:   Slider
        # Advancement: Note
        adv = StdScoreData._StdScoreData__ADV_NOTE
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 1000)

        map_time = 750

        # Time:        At slider release
        # Hitobject:   Slider
        # Advancement: No operation
        adv = StdScoreData._StdScoreData__ADV_NOP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 750)

        # Time:        At slider release
        # Hitobject:   Slider 
        # Advancement: Aimpoint
        adv = StdScoreData._StdScoreData__ADV_AIMP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 1000)

        # Time:        At slider release
        # Hitobject:   Slider
        # Advancement: Note
        adv = StdScoreData._StdScoreData__ADV_NOTE
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 1000)

        map_time = 1000

        # Time:        At 2nd hitobject
        # Hitobject:   Circle
        # Advancement: No operation
        adv = StdScoreData._StdScoreData__ADV_NOP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 1000)

        # Time:        At 2nd hitobject
        # Hitobject:   Circle 
        # Advancement: Aimpoint
        adv = StdScoreData._StdScoreData__ADV_AIMP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 1001)

        # Time:        At 2nd hitobject
        # Hitobject:   Circle
        # Advancement: Note
        adv = StdScoreData._StdScoreData__ADV_NOTE
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 2000)

        map_time = 2000

        # Time:        At last hitobject
        # Hitobject:   Circle
        # Advancement: No operation
        adv = StdScoreData._StdScoreData__ADV_NOP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 2000)

        # Time:        At last hitobject
        # Hitobject:   Circle 
        # Advancement: Aimpoint
        adv = StdScoreData._StdScoreData__ADV_AIMP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 2001)

        # Time:        At last hitobject
        # Hitobject:   Circle
        # Advancement: Note
        adv = StdScoreData._StdScoreData__ADV_NOTE
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 2002)

        map_time = 2001

        # Time:        At last scorepoint
        # Hitobject:   Circle
        # Advancement: No operation
        adv = StdScoreData._StdScoreData__ADV_NOP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 2001)

        # Time:        At last hitobject
        # Hitobject:   Circle 
        # Advancement: Aimpoint
        adv = StdScoreData._StdScoreData__ADV_AIMP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 2002)

        # Time:        At last hitobject
        # Hitobject:   Circle
        # Advancement: Note
        adv = StdScoreData._StdScoreData__ADV_NOTE
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 2002)

        map_time = 3000

        # Time:        After last hitobject
        # Hitobject:   Circle
        # Advancement: No operation
        adv = StdScoreData._StdScoreData__ADV_NOP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 3000)

        # Time:        After last hitobject
        # Hitobject:   Circle 
        # Advancement: Aimpoint
        adv = StdScoreData._StdScoreData__ADV_AIMP
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 2002)

        # Time:        After last hitobject
        # Hitobject:   Circle
        # Advancement: Note
        adv = StdScoreData._StdScoreData__ADV_NOTE
        new_map_time = StdScoreData._StdScoreData__adv(self.map_data, map_time, adv)
        self.assertEqual(new_map_time, 2002)


    def test_process_press(self):
        pass


    def test_process_hold(self):
        pass


    def test_process_release(self):
        pass


    '''
    def test_get_score_data(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests/maps/osu/test/score_test_new.osu')
        map_data = StdMapData.get_map_data(beatmap.hitobjects)
        #replay = ReplayIO.open_replay('unit_tests/replays/osu/score_test/autoplay.osr')
        replay = ReplayIO.open_replay('unit_tests/replays/osu/score_test/best_play.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, map_data)
    '''

    '''
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


    def test_playable_scores(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\playable\\LeaF - I (Maddy) [Terror].osu')
        map_data = StdMapData.get_map_data(beatmap.hitobjects)
        replay = ReplayIO.open_replay('unit_tests/replays/osu/LeaF - I (Maddy) [Terror] replay_0.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, map_data)

        tap_offset_mean = StdScoreData.tap_offset_mean(score_data)
        cursor_pos_offset_mean = StdScoreData.cursor_pos_offset_mean(score_data)
        print('LeaF - I (Maddy) [Terror] replay_0:', tap_offset_mean, cursor_pos_offset_mean)

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\playable\\Nakamura Meiko - Aka no Ha (Lily Bread) [Extra].osu')
        map_data = StdMapData.get_map_data(beatmap.hitobjects)
        replay = ReplayIO.open_replay('unit_tests/replays/osu/so bad - Nakamura Meiko - Aka no Ha [Extra] (2020-03-01) std Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, map_data)

        tap_offset_mean = StdScoreData.tap_offset_mean(score_data)
        cursor_pos_offset_mean = StdScoreData.cursor_pos_offset_mean(score_data)
        print('so bad - Nakamura Meiko - Aka no Ha [Extra] (2020-03-01) std Osu:', tap_offset_mean, cursor_pos_offset_mean)

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\playable\\Within Temptation - The Unforgiving (Armin) [Marathon].osu')
        map_data = StdMapData.get_map_data(beatmap.hitobjects)
        replay = ReplayIO.open_replay('unit_tests/replays/osu/Toy - Within Temptation - The Unforgiving [Marathon] (2018-02-06) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        score_data = StdScoreData.get_score_data(replay_data, map_data)

        tap_offset_mean = StdScoreData.tap_offset_mean(score_data)
        cursor_pos_offset_mean = StdScoreData.cursor_pos_offset_mean(score_data)
        print('Toy - Within Temptation - The Unforgiving [Marathon] (2018-02-06) Osu:', tap_offset_mean, cursor_pos_offset_mean)
    '''