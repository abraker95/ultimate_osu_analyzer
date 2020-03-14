from osu.local.replay.replayIO import ReplayIO


class ReplayReadTests():

    @staticmethod
    def test_replay_loading(filepath):
        replay = ReplayIO.open_replay(filepath)

        print(f'Player: {replay.player_name}')
        print(f'Score: {replay.score}   Combo: {replay.max_combo}   PF: {replay.is_perfect_combo}')
        print(f'Hits: {replay.number_300s}/{replay.gekis}/{replay.number_100s}/{replay.katus}/{replay.number_50s}/{replay.misses}')
        print()