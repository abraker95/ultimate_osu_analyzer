from misc.json_obj import JsonObj
from osu.online.osu_online import OsuOnline
from osu.online.osu_api import OsuApi

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.replay.replayIO import ReplayIO


class WebBeatmapset(JsonObj):

    def __init__(self, data):
        JsonObj.__init__(self, data)
        self.name = self.artist + ' - ' + self.title + ' (' + self.creator + ') '


    def get_beatmaps(self):
        return [ WebBeatmap(self.name, beatmap) for beatmap in self.beatmaps ]
        


class WebBeatmap(JsonObj):
    
    def __init__(self, name, data):
        JsonObj.__init__(self, data)
        self.name = name + '[' + self.version + ']'


    def get_scores(self):
        return [ WebScore(self.name, score) for score in OsuOnline.fetch_scores(self.id, self.mode) ]


    def download_beatmap(self, filepath):
        beatmap_data = OsuOnline.fetch_beatmap_file(self.id)
        pathname     = filepath + '/' + self.name + '.osu'
        BeatmapIO.save_beatmap(beatmap_data, pathname)


    def get_beatmap_data(self):
        return OsuOnline.fetch_beatmap_file(self.id, strio=True)



class WebScore(JsonObj):

    def __init__(self, name, data):
        JsonObj.__init__(self, data)
        self.name = name + ' ~ ' + self.user['username']
        if len(self.mods) > 0:  
            self.name += ' +' + ''.join(self.mods)


    def download_replay_api(self, filepath):
        replay_data = OsuApi.fetch_replay_file(self.id, self.user['username'], self.mode, self.mods)
        pathname    = filepath + '/' + self.name + '.osr'
        ReplayIO.save_replay(replay_data, pathname)


    def get_replay_data_api(self):
        return OsuApi.fetch_replay_file(self.id, self.user['username'], self.mode, self.mods)


    def download_replay_web(self, filepath):
        replay_data = OsuApi.fetch_replay_file(self.beatmap['id'], self.user['username'], self.mode, self.mods)
        pathname    = filepath + '/' + self.name + '.osr'
        ReplayIO.save_replay(replay_data, pathname)


    def get_replay_data_web(self):
        return OsuOnline.fetch_replay_file(self.id)