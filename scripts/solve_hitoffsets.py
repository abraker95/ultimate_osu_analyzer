import os
import pyqtgraph as pygraph


class SolveHitoffsets():

    def run(self, beatmap_name):
        replay_path = f'download/osu/replays/{beatmap_name}'
        replay_filenames = [ f for f in os.listdir(replay_path) if os.path.isfile(os.path.join(replay_path, f)) ]
        replay_filepaths = [ f'{replay_path}/{replay_filename}' for replay_filename in replay_filenames ]

        print('Loading map...')
        beatmap_filepath = f'download/osu/maps/{beatmap_name}.osu'
        beatmap = BeatmapIO.open_beatmap(beatmap_filepath)
        print('Loading map data...')
        map_data = StdMapData.get_aimpoint_data(beatmap.hitobjects)

        print('Loading replays...')
        replays = [ ReplayIO.open_replay(replay_filepath) for replay_filepath in replay_filepaths ]
        print('Loading replay data...')
        replay_data = [ StdReplayData.get_replay_data(replay.play_data) for replay in replays ]

        print('Loading scores...')
        score_data_array = np.asarray([ StdScoreData.get_score_data(data, map_data) for data in replay_data ])
        per_hitobject_score_data = StdScoreMetrics.get_per_hitobject_score_data(score_data_array)

        times, hit_offsets = StdScoreMetrics.solve_for_hit_offset_all(per_hitobject_score_data)

        win = pygraph.GraphicsWindow(title='Graph')
        win.resize(1000, 600)

        hit_offset_plot = win.addPlot(title='50% Hit offsets')
        hit_offset_plot = hit_offset_plot.plot(pen='y')
        hit_offset_plot.setData(times, hit_offsets)
        win.show()

        return win