import math
import pyqtgraph


class HitOffsets():

    def run(self, replay=None):
        replay_idx = 0 if replay==None else replay

        # Data extraction
        map_data    = StdMapData.get_aimpoint_data(get_beatmap().hitobjects)
        replay_data = get_replay_data()[replay_idx]
        score_data  = StdScoreData.get_score_data(replay_data, map_data)

        timing_data    = score_data[:, 0]
        hitoffset_data = score_data[:, 2]

        # GFX
        win = pyqtgraph.GraphicsWindow(title=get_beatmap().metadata.name + ' ' + get_replays()[replay_idx].get_name())
        win.resize(1000, 600)

        # Scatter plot showing hits
        hit_offset_scatter_plot = win.addPlot(title='Hits scatterplot')
        hit_offset_scatter_plot.addLine(x=None, y=0, pen=pyqtgraph.mkPen('r', width=1))
        hit_offset_scatter_plot.setLabel('left', 'Hit offset', units='ms', unitPrefix='')
        hit_offset_scatter_plot.setLabel('bottom', 'Time since start', units='ms', unitPrefix='')

        scatter_data_plot = hit_offset_scatter_plot.plot()
        scatter_data_plot.setData(timing_data, hitoffset_data, pen=None, symbol='o', symbolPen=None, symbolSize=2, symbolBrush=(100, 100, 255, 200))

        win.nextRow()

        # Plotting distribution of hits
        vec_normal_distr = np.vectorize(self.__normal_distr)
        avg = np.mean(hitoffset_data)
        std = np.std(hitoffset_data)

        hits = np.arange(-200, 200)
        pdf  = vec_normal_distr(hits, avg, std)

        hit_offset_model_plot = win.addPlot(title='Hits distribution')
        hit_offset_model_plot.setLabel('left', '# of hits', units='', unitPrefix='')
        hit_offset_model_plot.setLabel('bottom', 'Hit offset', units='ms', unitPrefix='')

        freqs = pyqtgraph.pseudoScatter(np.hstack(hitoffset_data), spacing=1)
        hit_offset_distr_plot = hit_offset_model_plot.plot()
        hit_offset_distr_plot.setData(hitoffset_data, freqs, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,150), symbolBrush=(0,0,255,150))

        model_data_plot = hit_offset_model_plot.plot(pen='y')
        model_data_plot.setData(hits, pdf*len(hitoffset_data))


        win.show()
        return win


    def __normal_distr(self, x, avg, std):
        return 1/(std*((2*math.pi)**0.5))*math.exp(-0.5*((x - avg)/std)**2)