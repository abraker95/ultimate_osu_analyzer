import unittest

from osu.local.replay.replayIO import ReplayIO

from analysis.osu.std.replay_data import StdReplayData



class TestStdReplayData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #cls.reply = ReplayIO
        pass


    @classmethod
    def tearDown(cls):  
        pass


    def test_get_replay_data(self):
        # TODO
        pass    def test_press_times(self):
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