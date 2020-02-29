
import os


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        try: os.mkdir(dir_path)
        except OSError: print(f'failed to create folder: {dir_path}')    


def run():
    try: beatmap_id
    except: 
        print('Please assign beatmap_id variable in embedded console')
        return
    
    create_dir('download/osu')
    create_dir('download/osu/maps')
    create_dir('download/osu/replays')

    beatmap = CmdOnline.get_beatmap(beatmap_id, 0)
    if beatmap == None: 
        print('Unable to get beatmap')
        return

    beatmap_name, beatmap_data = beatmap
    create_dir(f'download/osu/maps/{beatmap_name}')
    create_dir(f'download/osu/replays/{beatmap_name}')

    file_pathname = f'download/osu/maps/{beatmap_name}.osu'
    with open(file_pathname, 'w') as f:
        f.write(beatmap_data)

    scores = CmdOnline.get_scores(beatmap_id, 0)
    for score in scores:
        file_pathname = f'download/osu/replays/{beatmap_name}/{str(score)}.osr'
        with open(file_pathname, 'wb') as f:
            f.write(score.get_replay_data_web())


run()