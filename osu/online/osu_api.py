import base64
import urllib.request
import datetime
import hashlib 
import struct
import json
import time
import os

from osu.local.beatmap.beatmap import Beatmap
from osu.online.login import api_key



class OsuApi():

    REPLAY_RATE_FETCHING_LIMIT = 10  # seconds

    '''
    Returns the LZMA stream containing the cursor and key data, not the full *.osr file
    '''
    @staticmethod
    def fetch_replay_stream(user_name, beatmap_id, gamemode):
        param = []
        param.append('k=' + str(api_key))
        param.append('m=' + str(gamemode))
        param.append('b=' + str(beatmap_id))
        param.append('u=' + str(user_name))

        url = 'https://osu.ppy.sh/api/get_replay?'
        url += '&'.join(param)

        try:    time_passed = time.clock() - OsuApi.fetch_replay_stream.last_run_time
        except: time_passed = OsuApi.REPLAY_RATE_FETCHING_LIMIT + 1
            
        if time_passed < OsuApi.REPLAY_RATE_FETCHING_LIMIT:
            raise Exception('Please wait ' + str(round(10 - time_passed, 2)) + ' more seconds until fetching a replay again')
        OsuApi.fetch_replay_stream.last_run_time = time.clock()

        data = urllib.request.urlopen(url).read()
        try:    
            base_64 = json.loads(data.decode('utf-8'))
            return base64.b64decode(base_64['content'])
        except: 
            error = json.loads(data.decode('utf-8'))
            raise Exception(error['error'])

    
    @staticmethod
    def fetch_beatmap_info(beatmap_id):
        param = []
        param.append('k=' + str(api_key))
        param.append('b=' + str(beatmap_id))

        url = 'https://osu.ppy.sh/api/get_beatmaps?'
        url += '&'.join(param)

        data = urllib.request.urlopen(url).read()
        return json.loads(data.decode('utf-8'))


    @staticmethod
    def fetch_score_info(beatmap_id, user_name=None, gamemode=None, mods=None):
        param = []
        param.append('k=' + str(api_key))
        param.append('b=' + str(beatmap_id))
        
        if user_name != None: param.append('u=' + str(user_name))
        if gamemode  != None: param.append('m=' + str(gamemode))
        if mods      != None: param.append('mods=' + str(mods))

        url = 'https://osu.ppy.sh/api/get_scores?'
        url += '&'.join(param)

        data = urllib.request.urlopen(url).read()
        return json.loads(data.decode('utf-8'))


    # Thanks https://github.com/Xferno2/CSharpOsu/blob/master/CSharpOsu/CSharpOsu.cs
    @staticmethod
    def fetch_replay_file(user_name, beatmap_id, gamemode, mods):
        replay_data  = OsuApi.fetch_replay_stream(user_name, beatmap_id, gamemode)
        beatmap_info = OsuApi.fetch_beatmap_info(beatmap_id)[0]
        score_info   = OsuApi.fetch_score_info(beatmap_id, user_name=user_name, gamemode=gamemode, mods=mods)[0]

        version     = 0
        rank        = score_info['rank']
        count_300   = score_info['count300']
        count_100   = score_info['count100']
        count_50    = score_info['count50']
        count_geki  = score_info['countgeki']
        count_katsu = score_info['countkatu']
        count_miss  = score_info['countmiss']
        score       = score_info['score']
        max_combo   = score_info['maxcombo']
        perfect     = score_info['perfect']
        mods        = score_info['enabled_mods']
        lifebar_hp  = ''
        score_date  = score_info['date']
        score_id    = score_info['score_id']

        beatmap_md5 = beatmap_info['file_md5']
        replay_hash = hashlib.md5(str(max_combo + 'osu' + user_name + beatmap_md5 + score + rank).encode('utf-8')).hexdigest()

        data =  struct.pack('<bi', int(gamemode), int(version))
        data += struct.pack('<x' + str(len(beatmap_md5)) + 'sx', str(beatmap_md5).encode('utf-8'))
        data += struct.pack('<x' + str(len(user_name))   + 'sx', str(user_name).encode('utf-8'))
        data += struct.pack('<x' + str(len(replay_hash)) + 'sx', str(replay_hash).encode('utf-8'))
        data += struct.pack('<hhhhhhih?i',
            int(count_300), int(count_100), int(count_50), int(count_geki), int(count_katsu), int(count_miss),
            int(score), int(max_combo), int(perfect), int(mods))
        data += struct.pack('<x' + str(len(lifebar_hp)) + 'sx', str(lifebar_hp).encode('utf-8'))

        score_date, score_time = score_date.split(' ')
        score_year, score_month, score_day = score_date.split('-')
        score_hour, score_min, score_sec   = score_time.split(':')
        timestamp = datetime.datetime.timestamp(datetime.datetime(int(score_year), month=int(score_month), day=int(score_day), hour=int(score_hour), minute=int(score_min), second=int(score_sec)))
        
        data += struct.pack('<qi', int(timestamp), int(len(replay_data)))
        data += replay_data
        data += struct.pack('<q', int(score_id))

        return data


    @staticmethod
    def fetch_replays_from_map(beatmap_id, gamemode, mods):
        score_info = OsuApi.fetch_score_info(api_key, beatmap_id, gamemode-gamemode, mods=mods)
        replays    = []
        error      = False        
        for i in range(len(score_info)):
            score = score_info[i]
            print('(%i/%i) Gettings replay for %s' % (i, len(score_info), str(score['username'])))

            try: 
                replays.append(OsuApi.fetch_replay_file(api_key, score['username'], beatmap_id, gamemode, mods))
                error = False
            except urllib.error.HTTPError:
                if error: break
                i -= 1  # Try again
                error = True

            time.sleep(10)

        return replays