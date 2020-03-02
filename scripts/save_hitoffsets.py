
import os


'''
This script takes a beatmap file and a bunch of replays, calculates hitoffsets for each replay and saves them
to a *.csv file. This script works for std gamemode only.
'''
class SaveHitoffsets():
    def create_dir(self, dir_path):
        if not os.path.exists(dir_path):
            try: os.mkdir(dir_path)
            except OSError: print(f'failed to create folder: {dir_path}')    


    def run(self, beatmap_name, beatmap_filepath, replay_folder):
        self.create_dir('download/osu/hitoffsets')
        self.create_dir(f'download/osu/hitoffsets/{beatmap_name}')

        replay_filenames = [ f for f in os.listdir(replay_folder) if os.path.isfile(os.path.join(replay_folder, f)) ]
        replay_filepaths = [ f'{replay_folder}/{replay_filename}' for replay_filename in replay_filenames ]

        print('Loading map...')
        beatmap = BeatmapIO.open_beatmap(beatmap_filepath)
        print('Loading map data...')
        map_data = StdMapData.get_aimpoint_data(beatmap.hitobjects)

        print('Loading replays...')
        replays = [ ReplayIO.open_replay(replay_filepath) for replay_filepath in replay_filepaths ]
        print('Loading replay data...')
        replay_data = [ StdReplayData.get_replay_data(replay.play_data) for replay in replays ]

        print('Loading scores...')
        score_data = [ StdScoreData.get_score_data(data, map_data) for data in replay_data ]

        for replay_filename, score in zip(replay_filenames, score_data):
            replay_filename = replay_filename.split('.')[0]
            data = score[:, [StdScoreDataEnums.TIME.value, StdScoreDataEnums.HIT_OFFSET.value ]]
            CmdUtils.export_csv(f'download/osu/hitoffsets/{beatmap_name}/{replay_filename}', data.T)