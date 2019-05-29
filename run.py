import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.frames.main_frame import MainFrame

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.beatmap.beatmap import Beatmap

from osu.local.replay.replayIO import ReplayIO

from osu.online.osu_api import OsuApi
from osu.online.osu_online import OsuOnline

from cli.cmd_utils import CmdUtils
from cli.cmd_osu import CmdOsu
from cli.cmd_online import CmdOnline

from core.gamemode_manager import gamemode_manager
from core.layer_manager import LayerManager

from gui.objects.display import Display

from gui.objects.layer.layers.data_2d_layer import Data2DLayer
from gui.objects.layer.layers.std.hitobject_outline_layer import HitobjectOutlineLayer
from gui.objects.layer.layers.std.hitobject_aimpoint_layer import HitobjectAimpointLayer

from gui.objects.layer.layers.std.replay_layer import StdReplayLayer

from gui.objects.layer.layers.mania.raw_replay_layer import ManiaRawReplayLayer
from gui.objects.layer.layers.mania.press_replay_layer import ManiaPressReplayLayer
from gui.objects.layer.layers.mania.release_replay_layer import ManiaReleaseReplayLayer
from gui.objects.layer.layers.mania.hold_replay_layer import ManiaHoldReplayLayer

from gui.objects.layer.layers.mania.hitobject_render_layer import HitobjectRenderLayer

from gui.widgets.graph_manager import GraphManager
from gui.widgets.data_2d_graph import Data2DGraph
from gui.widgets.data_2d_temporal_graph import Data2DTemporalGraph

from analysis.osu.std.map_data import StdMapData
from analysis.osu.mania.map_data import ManiaMapData

from analysis.osu.std.map_metrics import StdMapMetrics



class MainWindow(QMainWindow):

    title = 'Ultimate osu! Analyzer'
    left   = 100
    top    = 100
    width  = 1500
    height = 720

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.main_frame = MainFrame() 
        self.menubar    = self.menuBar()

        self.file_menu           = self.menubar.addMenu('&File')
        self.open_beatmap_action = QAction("&Open beatmap", self)
        self.open_replay_action  = QAction("&Open replay", self)
        self.close_action        = QAction("&Quit w", self)

        self.view_menu              = self.menubar.addMenu('&View')
        self.graphs_menu            = self.view_menu.addMenu('&Graphs')
        self.view_velocity          = QAction("&velocity", self)
        self.view_tapping_intervals = QAction("&tapping intervals", self)
        
        self.toolbar    = self.addToolBar('Exit')
        self.status_bar = self.statusBar()

        self.timeline                 = self.main_frame.bottom_frame.timeline
        self.graph_manager_switch_gui = self.main_frame.center_frame.right_frame.graph_manager_switch
        self.analysis_controls        = self.main_frame.center_frame.right_frame.analysis_controls
        self.layer_manager_switch_gui = self.main_frame.center_frame.right_frame.layer_manager_switch
        self.ipython_console          = self.main_frame.center_frame.right_frame.ipython_console
        self.map_manager              = self.main_frame.center_frame.mid_frame.map_manager
        self.display                  = self.main_frame.center_frame.mid_frame.display


    def construct_gui(self):
        self.setCentralWidget(self.main_frame)
        self.toolbar.addAction(QAction(QIcon('new.bmp'), 'test menubar button', self))

        self.file_menu.addAction(self.open_beatmap_action)
        self.file_menu.addAction(self.open_replay_action)
        self.file_menu.addAction(self.close_action)
        
        self.open_beatmap_action.setStatusTip('Open *.osu beatmap for analysis')
        self.open_beatmap_action.setShortcut('Ctrl+N')
        self.open_beatmap_action.triggered.connect(self.request_open_beatmap)

        self.open_replay_action.setStatusTip('Open *.osr replay for analysis')
        self.open_replay_action.setShortcut('Shift+Ctrl+N')
        self.open_replay_action.triggered.connect(self.request_open_replay)

        self.close_action.setStatusTip('Quit the application')
        self.close_action.setShortcut('Ctrl+Q')
        self.close_action.triggered.connect(self.close_application)

        self.view_velocity.setCheckable(True)
        self.view_velocity.triggered.connect(self.view_velocity_action)

        self.view_tapping_intervals.setCheckable(True)
        self.view_tapping_intervals.triggered.connect(self.view_tapping_intervals_action)

        self.analysis_controls.create_graph_event.connect(self.graph_manager_switch_gui.add_graph)
        self.map_manager.map_changed_event.connect(self.change_map)
        self.map_manager.map_close_event.connect(self.close_map)

        # Allows to forward signals from any temporal graph without having means to get the instance
        Data2DTemporalGraph.__init__.connect(self.temporal_graph_creation_event)
        Data2DTemporalGraph.__del__.connect(self.temporal_graph_deletion_event)

        self.layer_manager_switch_gui.switch.connect(lambda old, new: self.display.setScene(new), inst=self.layer_manager_switch_gui)
        # gamemode_manger.switch.connect(self.)    # puts out MetricManager


    def update_gui(self):
        self.setAcceptDrops(True)
        self.setWindowTitle(MainWindow.title)
        self.setGeometry(MainWindow.left, MainWindow.top, MainWindow.width, MainWindow.height)
        self.status_bar.showMessage('Statusbar test message')

        self.ipython_console.push_vars({ 'timeline' : self.timeline })
        self.ipython_console.push_vars({ 'get_beatmap' : self.map_manager.get_current_map })

        self.ipython_console.push_vars({ 'add_layer_2d_data' : self.add_layer_2d_data })
        self.ipython_console.push_vars({ 'add_graph_2d_data' : self.add_graph_2d_data })

        self.ipython_console.push_vars({ 'StdMapData'    : StdMapData })
        self.ipython_console.push_vars({ 'ManiaMapData'  : ManiaMapData })
        self.ipython_console.push_vars({ 'StdMapMetrics' : StdMapMetrics })

        #self.ipython_console.push_vars({ 'OsuApi'    : OsuApi })
        #self.ipython_console.push_vars({ 'OsuOnline' : OsuOnline })

        self.ipython_console.push_vars({ 'CmdUtils'  : CmdUtils })
        self.ipython_console.push_vars({ 'CmdOsu'    : CmdOsu })
        self.ipython_console.push_vars({ 'CmdOnline' : CmdOnline })

        self.ipython_console.push_vars({ 'open_beatmap' : self.open_beatmap })
        self.ipython_console.push_vars({ 'load_beatmap' : self.load_beatmap })
        self.ipython_console.push_vars({ 'save_beatmap' : BeatmapIO.save_beatmap })

        self.ipython_console.push_vars({ 'open_replay' : self.open_replay })
        self.ipython_console.push_vars({ 'load_replay' : self.load_replay })
        self.ipython_console.push_vars({ 'save_replay' : ReplayIO.save_replay })    # TODO: use Replay class instead of bytes

        self.show()


    def temporal_graph_creation_event(self, graph):
        # Since everything connects to the timeline, and the timeline is always existing,
        # it acts as a central updater for every other temporal graph
        self.timeline.time_changed_event.connect(graph.timeline_marker.setValue)
        graph.time_changed_event.connect(self.timeline.timeline_marker.setValue)


    def temporal_graph_deletion_event(self, graph):
        self.timeline.time_changed_event.disconnect(graph.timeline_marker.setValue)
        graph.time_changed_event.disconnect(self.timeline.timeline_marker.setValue)


    def request_open_beatmap(self):
        beatmap_filepaths = self.get_type_files('osu files (*.osu)')
        if not beatmap_filepaths: return

        for beatmap_filepath in beatmap_filepaths:
            self.open_beatmap(beatmap_filepath)


    def open_beatmap(self, beatmap_filepath):
        beatmap = BeatmapIO.open_beatmap(beatmap_filepath)
        self.apply_beatmap(beatmap)


    def load_beatmap(self, beatmap_data):
        beatmap = BeatmapIO.load_beatmap(beatmap_data)
        self.apply_beatmap(beatmap)


    def apply_beatmap(self, beatmap):
        self.map_manager.add_map(beatmap, beatmap.metadata.name)

        self.layer_manager_switch_gui.add(beatmap.metadata.name, LayerManager())
        self.layer_manager_switch_gui.switch(beatmap.metadata.name)

        # TODO: Adding layers will be one of things analysis manager does
        if beatmap.gamemode == Beatmap.GAMEMODE_OSU:
            self.layer_manager_switch_gui.get().add_layer('hitobjects', HitobjectOutlineLayer(beatmap, self.timeline.time_changed_event))
            self.layer_manager_switch_gui.get().add_layer('aimpoints', HitobjectAimpointLayer(beatmap, self.timeline.time_changed_event))

        if beatmap.gamemode == Beatmap.GAMEMODE_MANIA:
            self.layer_manager_switch_gui.get().add_layer('hitobjects', HitobjectRenderLayer(beatmap, self.timeline.time_changed_event))

        self.graph_manager_switch_gui.add(beatmap.metadata.name, GraphManager())
        self.graph_manager_switch_gui.switch(beatmap.metadata.name)

        # TODO
        # self.replay_manager_switch_gui.add(beatmap.metadata.name, ReplayManager())
        # self.replay_manager_switch_gui.switch(beatmap.metadata.name)


    def request_open_replay(self):
        replay_filepaths = self.get_type_files('osr files (*.osr)')
        if not replay_filepaths: return

        for replay_filepath in replay_filepaths:
            self.open_replay(replay_filepath)


    def open_replay(self, replay_filepath):
        replay = ReplayIO.open_replay(replay_filepath)
        self.apply_replay(replay)
        

    def load_replay(self, replay_data):
        replay = ReplayIO.load_replay(replay_data)
        self.apply_replay(replay)


    def apply_replay(self, replay):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Error')
        msg.setStandardButtons(QMessageBox.Ok)

        beatmap = self.map_manager.get_current_map()
        if not beatmap:
            msg.setText('Error opening replay\nOpen a beatmap before opening a replay.')
            msg.exec_()
            return
        
        ''' TODO: Get beatmap md5 working
        if not replay.is_md5_match(beatmap.metadata.beatmap_md5):
            msg.setText('Error opening replay\nTrying to load replay for the wrong beatmap.')
            msg.exec_()
            return
        '''

        ''' TODO: Implement replay manager
        # Add replay to a list of replays
        self.replay_manager_switch_gui.get().add_replay(replay)
        '''

        # TODO: Adding layers will be one of things analysis manager does
        if beatmap.gamemode == Beatmap.GAMEMODE_OSU:
            self.layer_manager_switch_gui.get().add_layer('replay', StdReplayLayer(replay, self.timeline.time_changed_event))

        if beatmap.gamemode == Beatmap.GAMEMODE_MANIA:
            num_columns = beatmap.difficulty.cs
            #self.layer_manager_switch_gui.get().add_layer('raw_replay',     ManiaRawReplayLayer((replay, num_columns), self.timeline.time_changed_event))
            #self.layer_manager_switch_gui.get().add_layer('press_replay',   ManiaPressReplayLayer((replay, num_columns), self.timeline.time_changed_event))
            #self.layer_manager_switch_gui.get().add_layer('release_replay', ManiaReleaseReplayLayer((replay, num_columns), self.timeline.time_changed_event))
            self.layer_manager_switch_gui.get().add_layer('hold_replay',    ManiaHoldReplayLayer((replay, num_columns), self.timeline.time_changed_event))


    def close_map(self, beatmap):
        self.layer_manager_switch_gui.rmv(beatmap.metadata.name)
        self.graph_manager_switch_gui.rmv(beatmap.metadata.name)


    def get_type_files(self, file_type):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters([ file_type ])
        file_dialog.selectNameFilter(file_type)
        
        if file_dialog.exec_():
            return file_dialog.selectedFiles()


    def change_map(self, beatmap):
        if not beatmap: return

        # TODO: Fix bug where changing from a new loaded map first time doesn't safe timeline data
        try: self.timeline.save()
        except: pass

        try: self.timeline.load(beatmap.metadata.name)
        except ValueError:
            # Get new timeline range
            min_time, max_time = beatmap.get_time_range()
            self.timeline.setRange(xRange=(min_time - 100, max_time + 100))
            self.timeline.setLimits(xMin=min_time - 1000, xMax=max_time + 1000)
            self.timeline.timeline_marker.setValue(min_time)
            self.timeline.save(beatmap.metadata.name)

        gamemode_manager.switch(beatmap.gamemode)
        self.layer_manager_switch_gui.switch(beatmap.metadata.name)
        self.graph_manager_switch_gui.switch(beatmap.metadata.name)


    def add_layer_2d_data(self, name, data_2d):
        self.layer_manager_switch_gui.get().add_layer(name, Data2DLayer(name, data_2d))


    def add_graph_2d_data(self, name, data_2d, temporal=False, plot_type=Data2DGraph.SCATTER_PLOT):
        if not temporal:
            self.graph_manager_switch_gui.get().add_graph(Data2DGraph(name, data_2d, plot_type))
        else:
            self.graph_manager_switch_gui.get().add_graph(Data2DTemporalGraph(name, data_2d, plot_type))


    def remove_layer(self, name):
        # TODO
        pass


    def dragEnterEvent(self, e):
        paths = e.mimeData().text()
        paths = paths.split('\n')

        if len(paths) > 1:
            paths = paths[:-1]

        valid = True
        for path in paths:
            path      = path.split('///')[1]
            file_type = path.split('.')[-1]
        
            if file_type not in ['osu', 'osr']:
                valid = False
                break

        if valid: e.accept()
        else:     e.ignore()


    def dropEvent(self, e):
        paths = e.mimeData().text()
        paths = paths.split('\n')

        if len(paths) > 1:
            paths = paths[:-1]
            
        for path in paths:
            path      = path.split('///')[1]
            file_type = path.split('.')[-1]
            
            if file_type == 'osu': self.open_beatmap(path)
            if file_type == 'osr': self.open_replay(path)


    def close_application(self):
        sys.exit()


    def view_velocity_action(self):
        if self.view_velocity.isChecked():
            # TODO: display graph
            pass
        else:
            # TODO: remove graph
            pass


    def view_tapping_intervals_action(self):
        if self.view_tapping_intervals.isChecked():
            # TODO: display graph
            pass
        else:
            # TODO: remove graph
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex  = MainWindow()
    sys.exit(app.exec_())