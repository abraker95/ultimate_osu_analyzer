
import os


'''
This script takes a beatmap ID (the difficulty one) and downloads the associated *.osu file and all nomod replays (if accessible). 
It returns beatmap name, where beatmap got saved, and directory where all the replays are saved. This script works for std gamemode only.
Uses a mix of web requests and api v1. Requires your api key filled in the `api_key` variable in osu/online/login.py as well as your
osu! login info in same file as well.
'''
class DownloadReplays():

    def create_dir(self, dir_path):
        if not os.path.exists(dir_path):
            try: os.mkdir(dir_path)
            except OSError: print(f'failed to create folder: {dir_path}')    


    def run(self, beatmap_id):
        self.create_dir('download')
        self.create_dir('download/osu')
        self.create_dir('download/osu/maps')
        self.create_dir('download/osu/replays')

        beatmap = CmdOnline.get_beatmap(beatmap_id)
        if beatmap == None: 
            print('Unable to get beatmap')
            return

        beatmap_name, beatmap_data = beatmap

        beatmap_pathname = f'download/osu/maps/{beatmap_name}.osu'
        with open(beatmap_pathname, 'w', encoding='utf-8') as f:
            f.write(beatmap_data)

        replay_path = f'download/osu/replays/{beatmap_name}'
        self.create_dir(replay_path)

        scores = CmdOnline.get_scores_api(beatmap_id, 0, 0)
        for score in scores:
            replay_pathname = f'{replay_path}/{str(score)}.osr'
            with open(replay_pathname, 'wb') as f:
                f.write(score.get_replay_data_web())

        return beatmap_name, beatmap_pathname, replay_path