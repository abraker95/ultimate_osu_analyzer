import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui

from osu.local.hitobject.std.std import Std

from gui.objects.graph.hitobject_plot import HitobjectPlot
from gui.objects.graph.timing_plot import TimingPlot
from gui.objects.graph.aim_plot import AimPlot
from gui.objects.graph.score_plot import ScorePlot



class TimingGraph():

    def run(self, beatmap_path, replay_path):
        self.graphs = {}

        self.__init_gui_elements()
        self.__construct_gui()
        self.__set_data(beatmap_path, replay_path)

        self.win.show()
        return self.win


    def __create_graph(self, graph_id=None, dock_name='', pos='bottom', widget=pyqtgraph.PlotWidget()):
        self.graphs[graph_id] = widget

        dock = pyqtgraph.dockarea.Dock(dock_name, size=(500,400))
        dock.addWidget(self.graphs[graph_id])
        self.area.addDock(dock, pos)


    def __init_gui_elements(self):
        self.win  = QtGui.QMainWindow()
        self.area = pyqtgraph.dockarea.DockArea()

        self.__create_graph(
            graph_id  = 'timing',
            dock_name = 'dock',
            pos       = 'bottom',
            widget    = pyqtgraph.PlotWidget(title='Timing Graph'),
        )
        self.graphs['timing'].getViewBox().setMouseEnabled(y=False)


    def __construct_gui(self):
        self.win.setCentralWidget(self.area)


    def __set_data(self, beatmap_path, replay_path):
        beatmap = BeatmapIO.open_beatmap(beatmap_path)
        map_data = StdMapData.get_map_data(beatmap.hitobjects)
        
        cs_px = Std.cs_to_px(beatmap.difficulty.cs)

        replay = ReplayIO.open_replay(replay_path)
        replay_data = StdReplayData.get_replay_data(replay.play_data)

        score_data = StdScoreData.get_score_data(replay_data, map_data)

        score_data_d = score_data[score_data['type'] != StdScoreData.TYPE_HITR]
        dist_x = score_data_d['replay_x'] - score_data_d['map_x']
        dist_y = score_data_d['replay_y'] - score_data_d['map_y']

        reduced_replay_data = StdReplayData.get_reduced_replay_data(replay_data, False, True)
        
        dists = (dist_x**2 + dist_y**2)**0.5
        nan_filter = dists.notnull()
        dists_xy = dists[nan_filter]
        dists_t  = score_data_d['map_t'][nan_filter]

        map_ts = StdMapData.start_times(map_data)
        map_te = StdMapData.end_times(map_data)
        map_ot = map_data['object'][map_data['type'] == StdMapData.TYPE_PRESS]

        replay_ts_k1 = StdReplayData.press_times(replay_data,   [ 'k1', 'm1' ])
        replay_te_k1 = StdReplayData.release_times(replay_data, [ 'k1', 'm1' ])

        replay_ts_k2 = StdReplayData.press_times(replay_data,   [ 'k2', 'm2' ])
        replay_te_k2 = StdReplayData.release_times(replay_data, [ 'k2', 'm2' ])

        keystate_ts = StdReplayData.press_times(reduced_replay_data,   [ 'k' ])
        keystate_te = StdReplayData.release_times(reduced_replay_data, [ 'k' ])

        self.graphs['timing'].getPlotItem().addItem(HitobjectPlot(map_ts, map_te, map_ot))
        self.graphs['timing'].getPlotItem().addItem(TimingPlot(replay_ts_k1, replay_te_k1, color=(255, 100, 100, 100), yoffset=-1))
        self.graphs['timing'].getPlotItem().addItem(TimingPlot(replay_ts_k2, replay_te_k2, color=(255, 100, 100, 100), yoffset=1))
        self.graphs['timing'].getPlotItem().addItem(TimingPlot(keystate_ts, keystate_te, color=(0, 100, 255, 100), yoffset=-2))
        self.graphs['timing'].getPlotItem().addItem(ScorePlot(score_data['map_t'], score_data['type']))
        self.graphs['timing'].getPlotItem().addItem(AimPlot(dists_t, dists_xy, cs_px))