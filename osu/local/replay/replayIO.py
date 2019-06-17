import osrparse
import os
from osu.local.replay.replay import Replay


class ReplayIO():

    """
    Opens a replay file and reads it

    Args:
        filepath: (string) filepath to the replay file to load
    """
    @staticmethod
    def open_replay(filepath=None):
        with open(filepath, 'rb') as replay_data:
            replay = Replay(replay_data.read())

        return replay


    """
    Loads replay data

    Args:
        replay_data: (string) contents of the replay file
    """
    @staticmethod
    def load_replay(replay_data):
        return Replay(replay_data)


    """
    Saves replay data to file

    Args:
        replay_data: (string) contents of the replay file
        filepath: (string) filepath where to save the replay data
    """
    @staticmethod
    def save_replay(replay_data, filepath):
        path = os.path.dirname(filepath)
        if not os.path.exists(path):
            os.makedirs(path)
            
        with open(filepath, 'wb') as f:
            f.write(replay_data)