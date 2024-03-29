import base64
import urllib.request
import json
import time
import os
import io

from osu.local.beatmap.beatmap import Beatmap
from osu.online.SessionMgr import SessionMgr
from osu.online.rate_limited import rate_limited


class OsuOnline():

    session_manager = None

    @staticmethod
    @rate_limited(rate_limit=0.5)
    def fetch_beatmap_file(beatmap_id, strio=False, ret_name=False):
        url      = 'https://osu.ppy.sh/osu/' + str(beatmap_id)
        response = urllib.request.urlopen(url)
        data     = response.read()
        
        if not ret_name:
            if not strio: return data.decode('utf-8')
            else:         return io.StringIO(data.decode('utf-8'))

        name = response.info().get_filename()
        if name == None:
            print('Beatmap does not exist!')
            return

        if not strio: return name[1:].split('.')[0], data.decode('utf-8')
        else:         return name[1:].split('.')[0], io.StringIO(data.decode('utf-8'))


    @staticmethod
    @rate_limited(rate_limit=0.5)
    def fetch_beatmap_name(beatmap_id):
        url      = 'https://osu.ppy.sh/osu/' + str(beatmap_id)
        response = urllib.request.urlopen(url)
        name     = response.info().get_filename()
        
        return name[1:].split('.')[0]

    
    @staticmethod
    @rate_limited(rate_limit=3)
    def fetch_scores(beatmap_id, gamemode):
        if type(gamemode) == int:
            if   gamemode == Beatmap.GAMEMODE_OSU:   gamemode = 'osu'
            elif gamemode == Beatmap.GAMEMODE_TAIKO: gamemode = 'taiko'
            elif gamemode == Beatmap.GAMEMODE_CATCH: gamemode = 'fruits'
            elif gamemode == Beatmap.GAMEMODE_MANIA: gamemode = 'mania'
            else: raise Exception('Unknown gamemode: ' + str(gamemode))
        
        url = 'https://osu.ppy.sh/beatmaps/' + str(beatmap_id) + '/scores?type=global&mode=' + str(gamemode)
        try: response = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print('Error opening ' + url + '\n' + str(e))
            return

        data = json.loads(response.read())
        return data['scores']


    @staticmethod
    @rate_limited(rate_limit=3)
    def fetch_replay_file(gamemode, replay_id):
        if not SessionMgr.is_logged_in(): 
            SessionMgr.login()

        if not SessionMgr.is_logged_in(): 
            raise Exception('Not logged in')

        if type(gamemode) == int:
            if   gamemode == Beatmap.GAMEMODE_OSU:   gamemode = 'osu'
            elif gamemode == Beatmap.GAMEMODE_TAIKO: gamemode = 'taiko'
            elif gamemode == Beatmap.GAMEMODE_CATCH: gamemode = 'fruits'
            elif gamemode == Beatmap.GAMEMODE_MANIA: gamemode = 'mania'
            else: raise Exception('Unknown gamemode: ' + str(gamemode))

        url = 'https://osu.ppy.sh/scores/' + str(gamemode) + '/' + str(replay_id) + '/download'
        response = SessionMgr.fetch_web_data(url)

        return response.content


    # Only gets first 50 beatmapsets
    @staticmethod
    def fetch_latest_beatmapsets(gamemode, status):
        if not SessionMgr.is_logged_in(): 
            SessionMgr.login()

        if not SessionMgr.is_logged_in(): 
            raise Exception('Not logged in')

        url_param = [ 'm=' + str(gamemode) ]
        if status != None:
            url_param.append('s=' + str(status))

        url = 'https://osu.ppy.sh/beatmapsets/search?' + '&'.join(url_param)
        response = SessionMgr.fetch_web_data(url)

        return response.json()['beatmapsets']


    @staticmethod
    def fetch_latest_ranked_beatmaps(gamemode):
        latest_ranked_beatmapsets = OsuOnline.fetch_latest_ranked_beatmapsets(gamemode)
        for latest_ranked_beatmapset in latest_ranked_beatmapsets:
            title   = latest_ranked_beatmapset['title']
            artist  = latest_ranked_beatmapset['artist']
            creator = latest_ranked_beatmapset['creator']

            for difficulty in latest_ranked_beatmapset['beatmaps']:
                version = difficulty['version']

                name = artist + ' - ' + title + ' (' + creator + ') ' + '[' + version + ']'
                yield (name, difficulty)
                time.sleep(0.1)


    @staticmethod
    def fetch_latest_ranked_beatmap_files(gamemode):
        latest_ranked_beatmaps = OsuOnline.fetch_latest_ranked_beatmaps(gamemode)
        for latest_ranked_beatmap in latest_ranked_beatmaps:
                name, beatmap = latest_ranked_beatmap
                print('fetching ' + name)

                yield (name, OsuOnline.fetch_beatmap_file(beatmap['id']))
                time.sleep(0.5)


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
