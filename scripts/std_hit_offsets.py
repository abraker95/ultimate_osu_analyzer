import math
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui


class StdHitOffsets():

    def run(self, replay=None):
        replay_idx = 0 if replay==None else replay

        self.__init_gui_elements(replay_idx)
        self.__construct_gui()
        self.__set_data(replay_idx)

        self.win.show()
        return self.win


    def __init_gui_elements(self, replay_idx):
        self.win  = QtGui.QMainWindow() #pyqtgraph.GraphicsWindow(title=)
        self.area = pyqtgraph.dockarea.DockArea()

        self.dock_scatter           = pyqtgraph.dockarea.Dock('Scatterplot', size=(500,400))
        self.dock_offset_freq_distr = pyqtgraph.dockarea.Dock('Hit offset freq', size=(500,200))
        self.dock_offset_dist_distr = pyqtgraph.dockarea.Dock('Hit offset vs distance freq', size=(500,200))

        self.hit_offset_scatter_plot = pyqtgraph.PlotWidget(title='Hits scatterplot')
        self.hit_offset_distr_plot   = pyqtgraph.PlotWidget(title='Hits distribution')

        self.scatter_data_plot = self.hit_offset_scatter_plot.plot()
        self.distr_data_plot   = self.hit_offset_distr_plot.plot()
        self.model_data_plot   = self.hit_offset_distr_plot.plot()


    def __construct_gui(self):
        self.dock_offset_freq_distr.addWidget(self.hit_offset_scatter_plot)
        self.dock_offset_dist_distr.addWidget(self.hit_offset_distr_plot)

        self.area.addDock(self.dock_offset_freq_distr, 'top')
        self.area.addDock(self.dock_offset_dist_distr, 'bottom') 

        self.win.setCentralWidget(self.area)


    def __set_data(self, replay_idx):
        self.win.setWindowTitle(get_beatmap().metadata.name + ' ' + get_replays()[replay_idx].get_name())

        # Data extraction
        map_data    = StdMapData.get_map_data(get_beatmap().hitobjects)
        replay_data = get_replay_data()[replay_idx]
        score_data  = StdScoreData.get_score_data(replay_data, map_data)

        timing_data    = score_data['replay_t']
        hitoffset_data = score_data['replay_t'] - score_data['map_t']

        self.hit_offset_scatter_plot.addLine(x=None, y=0, pen=pyqtgraph.mkPen('r', width=1))
        self.hit_offset_scatter_plot.setLabel('left', 'Hit offset', units='ms', unitPrefix='')
        self.hit_offset_scatter_plot.setLabel('bottom', 'Time since start', units='ms', unitPrefix='')
        self.scatter_data_plot.setData(timing_data, hitoffset_data, pen=None, symbol='o', symbolPen=None, symbolSize=2, symbolBrush=(100, 100, 255, 200))

        # Plotting distribution of hits
        vec_normal_distr = np.vectorize(self.__normal_distr)
        avg = np.mean(hitoffset_data)
        std = np.std(hitoffset_data)

        freqs = pyqtgraph.pseudoScatter(np.hstack(hitoffset_data), spacing=1)
        
        self.distr_data_plot.setData(hitoffset_data, freqs, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,150), symbolBrush=(0,0,255,150))

        hits = np.arange(-200, 200)
        pdf = vec_normal_distr(hits, avg, std)

        self.hit_offset_distr_plot.setLabel('left', '# of hits', units='', unitPrefix='')
        self.hit_offset_distr_plot.setLabel('bottom', 'Hit offset', units='ms', unitPrefix='')
        self.model_data_plot.setData(hits, pdf*len(hitoffset_data), pen='y')


    def __normal_distr(self, x, avg, std):
        return 1/(std*((2*math.pi)**0.5))*math.exp(-0.5*((x - avg)/std)**2)