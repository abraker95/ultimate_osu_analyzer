import unittest

from osu.local.replay.replayIO import ReplayIO


class TestReplay(unittest.TestCase):

    def load_replay(self, filepath):
        try: replay = ReplayIO.open_replay(filepath)
        except: self.fail(f'Failed to load replay: {filepath}')

        print()
        print(f'Player: {replay.player_name}')
        print(f'Score: {replay.score}   Combo: {replay.max_combo}   PF: {replay.is_perfect_combo}')
        print(f'Hits: {replay.number_300s}/{replay.gekis}/{replay.number_100s}/{replay.katus}/{replay.number_50s}/{replay.misses}')
        print()


    def test_replay_loading(self):
        self.load_replay('unit_tests\\replays\\osu\\abraker - Mutsuhiko Izumi - Red Goose [ERT Basic] (2019-08-24) Osu.osr')
        self.load_replay('unit_tests\\replays\\osu\\LeaF - I (Maddy) [Terror] replay_0.osr')
        self.load_replay('unit_tests\\replays\\osu\\so bad - Nakamura Meiko - Aka no Ha [Extra] (2020-03-01) std Osu.osr')
        self.load_replay('unit_tests\\replays\\osu\\so bad - Nakamura Meiko - Aka no Ha [Extra] (2020-03-01) std ripple.osr')
        self.load_replay('unit_tests\\replays\\mania\\osu!topus! - DJ Genericname - Dear You [S.Star\'s 4K HD+] (2019-05-29) OsuMania.osr')
        self.load_replay('unit_tests\\replays\\osu\\Toy - Within Temptation - The Unforgiving [Marathon] (2018-02-06) Osu.osr')