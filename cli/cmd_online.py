from osu.online.osu_online import OsuOnline
from osu.online.osu_api import OsuApi
from osu.online.structs.web_structs import *
from osu.local.enums import MapStatus


class CmdOnline():

    @staticmethod
    def get_latest_beatmapsets(gamemode, status=MapStatus.Ranked):
        beatmapsets = OsuOnline.fetch_latest_beatmapsets(gamemode, status)
        return [ WebBeatmapset(beatmapset) for beatmapset in beatmapsets ]


    @staticmethod
    def get_beatmap(beatmap_id):
        return OsuOnline.fetch_beatmap_file(beatmap_id, ret_name=True)


    @staticmethod
    def get_scores(beatmap_id, mode, name=None):
        if name == None: name = OsuOnline.fetch_beatmap_name(beatmap_id)
        return [ WebScore(name, score) for score in OsuOnline.fetch_scores(beatmap_id, mode) ]


    @staticmethod
    def get_scores_api(beatmap_id, mode, mods, name=None):
        return OsuApi.fetch_score_info(beatmap_id, gamemode=mode, mods=mods)


    @staticmethod
    def get_scores_from_beatmap(beatmap):
        return CmdOnline.get_scores(beatmap.metadata.beatmap_id, beatmap.gamemode, beatmap.metadata.name)