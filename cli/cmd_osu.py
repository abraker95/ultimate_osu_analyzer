import time

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.replay.replayIO import ReplayIO


class CmdOsu():

    @staticmethod
    def open_replay_file(replay_filepath):
        return ReplayIO.open_replay(replay_filepath)
        

    @staticmethod
    def save_web_beatmaps(web_beatmaps):
        '''
        In: [ WebBeatmap, ... ]
        '''
        for web_beatmap in web_beatmaps:
            web_beatmap.download_beatmap('tmp/beatmaps/')
            time.sleep(0.1)


    @staticmethod
    def save_web_replays(web_replays):
        '''
        In: [ WebReplay, ... ]
        '''
        for web_replay in web_replays:
            web_replay.download_replay('tmp/replays/')
            time.sleep(10)