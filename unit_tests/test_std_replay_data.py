import unittest

from osu.local.replay.replayIO import ReplayIO
from analysis.osu.std.replay_data import StdReplayData



class TestStdReplayData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDown(cls):  
        pass


    def test_get_replay_data(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/LeaF - I (Maddy) [Terror] replay_0.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)

        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)

        replay = ReplayIO.open_replay('unit_tests/replays/osu/Toy - Within Temptation - The Unforgiving [Marathon] (2018-02-06) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)


    def test_press_times(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        press_times = StdReplayData.press_times(replay_data)

        self.assertEqual(len(press_times), 11)


    def test_release_times(self):
        replay = ReplayIO.open_replay('unit_tests/replays/osu/osu! - perfect_test [score_test] (2019-06-07) Osu.osr')
        replay_data = StdReplayData.get_replay_data(replay.play_data)
        release_times = StdReplayData.release_times(replay_data)

        self.assertEqual(len(release_times), 11)

    
    def test_get_key_state(self):
        # Shorthand
        FREE    = StdReplayData.FREE
        PRESS   = StdReplayData.PRESS
        HOLD    = StdReplayData.HOLD
        RELEASE = StdReplayData.RELEASE

        # free -> all free
        key_state = StdReplayData._StdReplayData__get_key_state(FREE, [ FREE, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, FREE)

        # TODO: this is an illegal state (you can't have a press transition into a free, it must go to a release first)
        #key_state = StdReplayData._StdReplayData__get_key_state(PRESS, [ FREE, FREE, FREE, FREE ], press_block=False, release_block=False)
        #self.assertEqual(key_state, )

        # TODO: this is an illegal state (you can't have a hold transition into a free, it must go to a release first)
        #key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ FREE, FREE, FREE, FREE ], press_block=False, release_block=False)
        #self.assertEqual(key_state, )

        # release -> all free
        key_state = StdReplayData._StdReplayData__get_key_state(RELEASE, [ FREE, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, FREE)

        # free -> one press
        key_state = StdReplayData._StdReplayData__get_key_state(FREE, [ PRESS, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # press -> one press
        key_state = StdReplayData._StdReplayData__get_key_state(PRESS, [ PRESS, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # hold -> one press (non blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ PRESS, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # hold -> one press (blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ PRESS, FREE, FREE, FREE ], press_block=True, release_block=False)
        self.assertEqual(key_state, HOLD)

        # TODO: this is an illegal state (you can't have a release transition into a press, it must go to a free first)
        #key_state = StdReplayData._StdReplayData__get_key_state(RELEASE, [ PRESS, FREE, FREE, FREE ], press_block=False, release_block=False)
        #self.assertEqual(key_state, )

        # TODO: this is an illegal state (you can't have a free transition into a hold, it must go to a press first)
        #key_state = StdReplayData._StdReplayData__get_key_state(FREE, [ HOLD, FREE, FREE, FREE ], press_block=False, release_block=False)
        #self.assertEqual(key_state, )

        # press -> one hold
        key_state = StdReplayData._StdReplayData__get_key_state(PRESS, [ HOLD, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, HOLD)

        # hold -> one hold
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ HOLD, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, HOLD)

        # TODO: this is an illegal state (you can't have a release transition into a hold, it must go to press first)
        #key_state = StdReplayData._StdReplayData__get_key_state(RELEASE, [ HOLD, FREE, FREE, FREE ], press_block=False, release_block=False)
        #self.assertEqual(key_state, )

        # press -> one release
        key_state = StdReplayData._StdReplayData__get_key_state(PRESS, [ RELEASE, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, RELEASE)

        # Test hold -> one release (non blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ RELEASE, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, RELEASE)

        # hold -> one release (blocking)      
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ RELEASE, FREE, FREE, FREE ], press_block=False, release_block=True)
        self.assertEqual(key_state, RELEASE)

        # release -> one release
        key_state = StdReplayData._StdReplayData__get_key_state(RELEASE, [ RELEASE, FREE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, FREE)

        # free -> one press, one release
        key_state = StdReplayData._StdReplayData__get_key_state(FREE, [ PRESS, RELEASE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # press -> one press, one release
        key_state = StdReplayData._StdReplayData__get_key_state(FREE, [ PRESS, RELEASE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # hold -> one press, one release (non blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ PRESS, RELEASE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # hold -> one press, one release (press blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ PRESS, RELEASE, FREE, FREE ], press_block=True, release_block=False)
        self.assertEqual(key_state, RELEASE)

        # hold -> one press, one release (release blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ PRESS, RELEASE, FREE, FREE ], press_block=False, release_block=True)
        self.assertEqual(key_state, PRESS)

        # hold -> one press, one release (press blocking, release blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ PRESS, RELEASE, FREE, FREE ], press_block=True, release_block=True)
        self.assertEqual(key_state, RELEASE)

        # hold -> one hold, one release (non blocking)        
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ HOLD, RELEASE, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, RELEASE)

        # hold -> one hold, one release (blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ HOLD, RELEASE, FREE, FREE ], press_block=False, release_block=True)
        self.assertEqual(key_state, HOLD)

        # hold -> release, hold (blocking)      
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ RELEASE, HOLD, FREE, FREE ], press_block=False, release_block=True)
        self.assertEqual(key_state, HOLD)

        # hold -> release, hold (not blocking)      
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ RELEASE, HOLD, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, RELEASE)

        # hold -> one hold, one press (not blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ HOLD, PRESS, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # hold -> one hold, one press (blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ HOLD, PRESS, FREE, FREE ], press_block=True, release_block=False)
        self.assertEqual(key_state, HOLD)

        # hold -> one hold, one press (not blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ PRESS, HOLD, FREE, FREE ], press_block=False, release_block=False)
        self.assertEqual(key_state, PRESS)

        # hold -> one hold, one press (blocking)
        key_state = StdReplayData._StdReplayData__get_key_state(HOLD, [ PRESS, HOLD, FREE, FREE ], press_block=True, release_block=False)
        self.assertEqual(key_state, HOLD)
