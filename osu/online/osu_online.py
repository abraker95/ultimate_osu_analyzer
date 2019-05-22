import base64
import urllib.request
import json
import time
import os

from osu.local.beatmap.beatmap import Beatmap



class OsuOnline():

    @staticmethod
    def fetch_beatmap_file(beatmap_id):
        url      = 'https://osu.ppy.sh/osu/' + str(beatmap_id)
        response = urllib.request.urlopen(url)
        data     = response.read()
        
        return data.decode('utf-8')

    
    @staticmethod
    def fetch_scores(beatmap_id, gamemode):
        if   gamemode == Beatmap.GAMEMODE_OSU:   gamemode = 'osu'
        elif gamemode == Beatmap.GAMEMODE_TAIKO: gamemode = 'taiko'
        elif gamemode == Beatmap.GAMEMODE_CATCH: gamemode = 'fruits'
        elif gamemode == Beatmap.GAMEMODE_MANIA: gamemode = 'mania'
        else: raise Exception('Unknown gamemode: ' + str(gamemode))

        url = 'https://osu.ppy.sh/beatmaps/' + str(beatmap_id) + '/scores?type=global&mode=' + str(gamemode)
        response = urllib.request.urlopen(url)
        return json.loads(response.read())


    @staticmethod
    def search_maps(statuses=[], gamemodes=[], title=None, artist=None, source=None, mapper=None, diff_name=None):
        url = 'https://osusearch.com/query/?'
        param = []
        
        if title  != None:    param.append('title=' + str(title))
        if artist != None:    param.append('artist=' + str(artist))
        if source != None:    param.append('source=' + str(source))
        if mapper != None:    param.append('mapper=' + str(mapper))
        if diff_name != None: param.append('diff_name=' + str(diff_name))

        # TODO: statuses
        # 'statuses=Ranked,Loved,Qualified,Unranked'

        # TODO: gamemodes
        # 'modes=Standard,Mania,Taiko,CtB'

        # TODO: date_start
        # 'date_start=2019-05-09'

        # TODO: date_end
        # 'date_end=2019-05-24'

        # TODO: min_lengh
        # 'min_length=3'

        # TODO: max_length
        # 'max_length=2'

        # TODO: min_bpm
        # 'min_bpm=2'

        # TODO: max_bpm
        # 'max_bpm=2'

        # TODO: min_favorites
        # 'min_favorites=2'

        # TODO: max_favorites
        # 'max_favorites=2'

        # TODO: min_play_count
        # 'max_play_count=2'

        # TODO: star
        # 'star=(2.80,10.00)'

        # TODO: ar
        # 'ar=(2.60,8.40)'

        # TODO: od
        # 'od=(3.30,8.20)'

        # TODO: cs
        # 'cs=(3.00,6.30)'

        # TODO: hp
        # 'hp=(3.40,6.20)'

        url += '&'.join(param)
        response = urllib.request.urlopen(url)
        return json.loads(response.read())
