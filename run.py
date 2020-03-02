import sys
import time
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.frames.main_frame import MainFrame

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.beatmap.beatmap import Beatmap
from osu.local.hitobject.std.std import Std, StdSettings
from osu.local.replay.replayIO import ReplayIO

from osu.online.osu_api import OsuApi
from osu.online.osu_online import OsuOnline

from cli.cmd_utils import CmdUtils
from cli.cmd_osu import CmdOsu
from cli.cmd_online import CmdOnline

from core.gamemode_manager import gamemode_manager

from gui.objects.display import Display

from gui.objects.layer.layers.std_data_2d_layer import StdData2DLayer
from gui.objects.layer.layers.mania_data_2d_layer import ManiaData2DLayer

from gui.objects.layer.layers.std.hitobject_outline_layer import HitobjectOutlineLayer
from gui.objects.layer.layers.std.hitobject_aimpoint_layer import HitobjectAimpointLayer

from gui.objects.layer.layers.std.replay_cursor_layer import StdReplayCursorLayer
from gui.objects.layer.layers.std.replay_hold_layer import StdReplayHoldLayer
from gui.objects.layer.layers.std.score_debug_layer import StdScoreDebugLayer

from gui.objects.layer.layers.mania.raw_replay_layer import ManiaRawReplayLayer
from gui.objects.layer.layers.mania.press_replay_layer import ManiaPressReplayLayer
from gui.objects.layer.layers.mania.release_replay_layer import ManiaReleaseReplayLayer
from gui.objects.layer.layers.mania.hold_replay_layer import ManiaHoldReplayLayer
from gui.objects.layer.layers.mania.score_debug_layer import ManiaScoreDebugLayer

from gui.objects.layer.layers.mania.hitobject_render_layer import HitobjectRenderLayer

from gui.widgets.layer_manager import LayerManager
from gui.widgets.replay_manager import ReplayManager
from gui.widgets.graph_manager import GraphManager
from gui.widgets.data_2d_graph import Data2DGraph
from gui.widgets.data_2d_temporal_graph import Data2DTemporalGraph

from gui.widgets.std_settings import StdSettingsGui
from gui.widgets.mania_settings import ManiaSettingsGui

from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.map_metrics import StdMapMetrics
from analysis.osu.std.replay_data import StdReplayData
from analysis.osu.std.replay_metrics import StdReplayMetrics
from analysis.osu.std.score_data import StdScoreData, StdScoreDataEnums
from analysis.osu.std.score_metrics import StdScoreMetrics
from analysis.osu.std.std_layers import StdLayers

from analysis.osu.mania.map_data import ManiaMapData
from analysis.osu.mania.map_metrics import ManiaMapMetrics
from analysis.osu.mania.replay_data import ManiaReplayData
from analysis.osu.mania.score_data import ManiaScoreData, ManiaScoreDataEnums
from analysis.osu.mania.mania_layers import ManiaLayers


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

        self.file_menu              = self.menubar.addMenu('&File')
        self.open_beatmap_action    = QAction("&Open beatmap", self)
        self.open_replay_action     = QAction("&Open replay", self)
        self.close_action           = QAction("&Quit w", self)

        self.view_menu              = self.menubar.addMenu('&View')
        self.graphs_menu            = self.view_menu.addMenu('&Graphs')
        self.view_velocity          = QAction("&velocity", self)
        self.view_tapping_intervals = QAction("&tapping intervals", self)
        
        self.options_menu           = self.menubar.addMenu('&Options')
        self.std_settings_action    = QAction("&Std settings", self)
        self.mania_settings_action  = QAction("&Mania settings", self)

        self.toolbar    = self.addToolBar('Exit')
        self.status_bar = self.statusBar()

        self.timeline                  = self.main_frame.bottom_frame.timeline
        self.layer_manager_switch_gui  = self.main_frame.center_frame.right_frame.layer_manager_switch
        self.replay_manager_switch_gui = self.main_frame.center_frame.right_frame.replay_manager_switch
        self.graph_manager_switch_gui  = self.main_frame.center_frame.right_frame.graph_manager_switch
        self.analysis_controls         = self.main_frame.center_frame.right_frame.analysis_controls
        self.ipython_console           = self.main_frame.center_frame.right_frame.ipython_console
        self.map_manager               = self.main_frame.center_frame.mid_frame.map_manager
        self.display                   = self.main_frame.center_frame.mid_frame.display


    def construct_gui(self):
        self.setCentralWidget(self.main_frame)
        self.toolbar.addAction(QAction(QIcon('new.bmp'), 'test menubar button', self))

        # File menu
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

        # View menu
        self.view_velocity.setCheckable(True)
        self.view_velocity.triggered.connect(self.view_velocity_action)

        self.view_tapping_intervals.setCheckable(True)
        self.view_tapping_intervals.triggered.connect(self.view_tapping_intervals_action)

        # Options menu
        self.options_menu.addAction(self.std_settings_action)
        self.options_menu.addAction(self.mania_settings_action)

        self.std_settings_action.triggered.connect(self.show_std_settings)
        self.mania_settings_action.triggered.connect(self.show_mania_settings)

        #self.analysis_controls.create_graph_event.connect(lambda: self.graph_manager_switch_gui.get().add_graph)
        self.map_manager.map_changed_event.connect(self.change_map)
        self.map_manager.map_close_event.connect(self.close_map)

        # Allows to forward signals from any temporal graph without having means to get the instance
        Data2DTemporalGraph.__init__.connect(self.temporal_graph_creation_event)
        Data2DTemporalGraph.__del__.connect(self.temporal_graph_deletion_event)

        self.layer_manager_switch_gui.switch.connect(self.set_scene, inst=self.layer_manager_switch_gui)

        CmdOsu.create_score_offset_graph.connect(self.create_score_offset_graph)
        CmdOsu.create_cursor_velocity_graph.connect(self.create_cursor_velocity_graph)
        CmdOsu.create_cursor_acceleration_graph.connect(self.create_cursor_acceleration_graph)
        CmdOsu.create_cursor_jerk_graph.connect(self.create_cursor_jerk_graph)


    def update_gui(self):
        self.setAcceptDrops(True)
        self.setWindowTitle(MainWindow.title)
        self.setGeometry(MainWindow.left, MainWindow.top, MainWindow.width, MainWindow.height)
        self.status_bar.showMessage('')

        self.ipython_console.execute_command('import numpy as np')
        self.ipython_console.execute_command('import matplotlib')
        self.ipython_console.execute_command('import matplotlib.pyplot as plt')
        self.ipython_console.execute_command('np.set_printoptions(suppress=True)')

        self.ipython_console.push_vars({ 'tick' : self.tick })

        self.ipython_console.push_vars({ 'BeatmapIO' : BeatmapIO })
        self.ipython_console.push_vars({ 'ReplayIO' : ReplayIO })

        self.ipython_console.push_vars({ 'timeline' : self.timeline })
        self.ipython_console.push_vars({ 'get_beatmap' : self.map_manager.get_current_map })
        self.ipython_console.push_vars({ 'get_replays' : lambda: self.replay_manager_switch_gui.get().get_replay_data() })

        self.ipython_console.push_vars({ 'add_std_layer'     : self.add_std_layer })
        self.ipython_console.push_vars({ 'add_mania_layer'   : self.add_mania_layer })
        self.ipython_console.push_vars({ 'add_graph_2d_data' : self.add_graph_2d_data })

        self.ipython_console.push_vars({ 'StdMapData'       : StdMapData })
        self.ipython_console.push_vars({ 'StdMapMetrics'    : StdMapMetrics })
        self.ipython_console.push_vars({ 'StdReplayData'    : StdReplayData })
        self.ipython_console.push_vars({ 'StdReplayMetrics' : StdReplayMetrics })
        self.ipython_console.push_vars({ 'StdScoreData'     : StdScoreData })
        self.ipython_console.push_vars({ 'StdScoreMetrics'  : StdScoreMetrics })
        self.ipython_console.push_vars({ 'StdLayers'        : StdLayers })

        self.ipython_console.push_vars({ 'StdScoreDataEnums'  : StdScoreDataEnums })
        self.ipython_console.push_vars({ 'Std'                : Std })
        self.ipython_console.push_vars({ 'StdSettings'        : StdSettings })

        self.ipython_console.push_vars({ 'ManiaMapData'    : ManiaMapData })
        self.ipython_console.push_vars({ 'ManiaMapMetrics' : ManiaMapMetrics })
        self.ipython_console.push_vars({ 'ManiaReplayData' : ManiaReplayData })
        self.ipython_console.push_vars({ 'ManiaScoreData'  : ManiaScoreData })
        self.ipython_console.push_vars({ 'ManiaLayers'     : ManiaLayers })

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
        self.status_bar.showMessage('Applying map "' + str(beatmap.metadata.name) + '"')

        self.map_manager.add_map(beatmap, beatmap.metadata.name)

        self.layer_manager_switch_gui.add(beatmap.metadata.name, LayerManager())
        self.layer_manager_switch_gui.switch(beatmap.metadata.name)

        self.replay_manager_switch_gui.add(beatmap.metadata.name, ReplayManager())
        self.replay_manager_switch_gui.switch(beatmap.metadata.name)

        # TODO: Adding layers will be one of things analysis manager does
        if beatmap.gamemode == Beatmap.GAMEMODE_OSU:
            self.layer_manager_switch_gui.get().add_layer('map', HitobjectOutlineLayer(beatmap, self.timeline.time_changed_event))
            self.layer_manager_switch_gui.get().add_layer('map', HitobjectAimpointLayer(beatmap, self.timeline.time_changed_event))

        if beatmap.gamemode == Beatmap.GAMEMODE_MANIA:
            self.layer_manager_switch_gui.get().add_layer('map', HitobjectRenderLayer(beatmap, self.timeline.time_changed_event))

        self.graph_manager_switch_gui.add(beatmap.metadata.name, GraphManager())
        self.graph_manager_switch_gui.switch(beatmap.metadata.name)


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

        self.status_bar.showMessage('Applying replay . . .')

        # Add replay to a list of replays
        self.replay_manager_switch_gui.get().add_replay(replay)

        # TODO: Adding layers will be one of things analysis manager does
        group = 'replay.' + str(replay.player_name)

        if beatmap.gamemode == Beatmap.GAMEMODE_OSU:
            self.layer_manager_switch_gui.get().add_layer(group, StdReplayCursorLayer(replay, self.timeline.time_changed_event))
            self.layer_manager_switch_gui.get().add_layer(group, StdReplayHoldLayer(replay, self.timeline.time_changed_event))
            #self.layer_manager_switch_gui.get().add_layer(group, StdScoreDebugLayer((beatmap, replay), self.timeline.time_changed_event))

        if beatmap.gamemode == Beatmap.GAMEMODE_MANIA:
            num_columns = beatmap.difficulty.cs
            #self.layer_manager_switch_gui.get().add_layer(group, ManiaRawReplayLayer((replay, num_columns), self.timeline.time_changed_event))
            #self.layer_manager_switch_gui.get().add_layer(group, ManiaPressReplayLayer((replay, num_columns), self.timeline.time_changed_event))
            #self.layer_manager_switch_gui.get().add_layer(group, ManiaReleaseReplayLayer((replay, num_columns), self.timeline.time_changed_event))
            self.layer_manager_switch_gui.get().add_layer(group, ManiaHoldReplayLayer((replay, num_columns), self.timeline.time_changed_event))
            self.layer_manager_switch_gui.get().add_layer(group, ManiaScoreDebugLayer((beatmap, replay), self.timeline.time_changed_event))

        self.status_bar.showMessage('Replay applied. Check replay tab.')


    def close_map(self, beatmap):
        self.status_bar.showMessage('Closing map "' + str(beatmap.metadata.name) + '"')

        self.layer_manager_switch_gui.rmv(beatmap.metadata.name)
        self.replay_manager_switch_gui.rmv(beatmap.metadata.name)
        self.graph_manager_switch_gui.rmv(beatmap.metadata.name)


    def get_type_files(self, file_type):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters([ file_type ])
        file_dialog.selectNameFilter(file_type)
        
        if file_dialog.exec_():
            return file_dialog.selectedFiles()


    def change_map(self, beatmap):
        if beatmap == None: return

        self.status_bar.showMessage('Switching to map "' + str(beatmap.metadata.name) + '"')

        # TODO: Fix bug where changing from a new loaded map first time doesn't safe timeline data
        try: self.timeline.save()
        except: pass

        min_time, max_time = beatmap.get_time_range()
        self.timeline.setLimits(xMin=min_time - 1000, xMax=max_time + 1000)

        try: self.timeline.load(beatmap.metadata.name)
        except ValueError:
            # Get new timeline range
            self.timeline.setRange(xRange=(min_time - 100, max_time + 100))
            self.timeline.timeline_marker.setValue(min_time)
            self.timeline.save(beatmap.metadata.name)

        gamemode_manager.switch(beatmap.gamemode)
        self.layer_manager_switch_gui.switch(beatmap.metadata.name)
        self.replay_manager_switch_gui.switch(beatmap.metadata.name)
        self.graph_manager_switch_gui.switch(beatmap.metadata.name)

        self.status_bar.showMessage('Switched to map "' + str(beatmap.metadata.name) + '"')

        # TODO: Multi gamemode support
        if beatmap.gamemode == Beatmap.GAMEMODE_OSU:
            self.timeline.set_map(beatmap)
        else:
            self.timeline.set_map(None)


    def add_std_layer(self, group, layer_name, data, draw_func):
        self.layer_manager_switch_gui.get().add_layer(group, StdData2DLayer(layer_name, data, draw_func, self.timeline.time_changed_event))


    def add_mania_layer(self, group, layer_name, columns, data, draw_func):
        self.layer_manager_switch_gui.get().add_layer(group, ManiaData2DLayer(layer_name, columns, data, draw_func, self.timeline.time_changed_event))


    def add_graph_2d_data(self, name, data_2d, temporal=False, plot_type=Data2DGraph.SCATTER_PLOT):
        if not temporal:
            self.graph_manager_switch_gui.get().add_graph(Data2DGraph(name, data_2d, plot_type))
        else:
            self.graph_manager_switch_gui.get().add_graph(Data2DTemporalGraph(name, data_2d, plot_type))


    def remove_layer(self, name):
        # TODO
        pass


    def tick(self, ms_sleep=0.1):
        QApplication.instance().processEvents()
        time.sleep(min(ms_sleep, 0.1))


    def set_scene(self, old_layer_mgr, new_layer_mgr):
        if new_layer_mgr != None:
            self.display.setScene(new_layer_mgr.get_scene())
        else:
            self.display.setScene(QGraphicsScene())


    def show_mania_settings(self):
        self.tmp = ManiaSettingsGui()
        self.tmp.show()

    
    def show_std_settings(self):
        self.tmp = StdSettingsGui()
        self.tmp.show()


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


    def create_score_offset_graph(self, replay_data):
        self.status_bar.showMessage('Creating replay hit offsets graph')

        gamemode = self.map_manager.get_current_map().gamemode
        hitobjects = self.map_manager.get_current_map().hitobjects

        if gamemode == Beatmap.GAMEMODE_OSU:
            aimpoint_data = StdMapData.get_aimpoint_data(hitobjects)
            score_data = StdScoreData.get_score_data(replay_data, aimpoint_data)
            times, offsets = score_data[:,StdScoreDataEnums.TIME.value], score_data[:,StdScoreDataEnums.HIT_OFFSET.value]
        #elif gamemode == Beatmap.GAMEMODE_TAIKO: 
        #    score_data = StdScoreData.get_score_data(replay_data, aimpoint_data)
        #elif gamemode == Beatmap.GAMEMODE_CATCH: 
        #    score_data = StdScoreData.get_score_data(replay_data, aimpoint_data)
        elif gamemode == Beatmap.GAMEMODE_MANIA: 
            map_data = ManiaMapData.get_hitobject_data(hitobjects)
            score_data = np.vstack(ManiaScoreData.get_score_data(replay_data, map_data))
            score_data = score_data[np.argsort(score_data[:,0])]
            times, offsets = score_data[:,ManiaScoreDataEnums.TIME.value], score_data[:,ManiaScoreDataEnums.HIT_OFFSET.value]
        else:
            RuntimeError('Unsupported gamemode')
        
        self.add_graph_2d_data('replay hit offsets', (times, offsets), temporal=True, plot_type=Data2DGraph.SCATTER_PLOT)
        self.status_bar.showMessage('Created replay hit offsets graph. Check graphs tab.')


    def create_cursor_velocity_graph(self, replay_data):
        self.status_bar.showMessage('Creating replay cursor velocity graph')

        velocity_data = StdReplayMetrics.cursor_velocity(replay_data)
        self.add_graph_2d_data('replay cursor velocity', velocity_data, temporal=True, plot_type=Data2DGraph.LINE_PLOT)

        self.status_bar.showMessage('Created replay cursor velocity graph. Check graphs tab.')


    def create_cursor_acceleration_graph(self, replay_data):
        self.status_bar.showMessage('Creating replay cursor acceleration graph')

        acceleration_data = StdReplayMetrics.cursor_acceleration(replay_data)
        self.add_graph_2d_data('replay cursor acceleration', acceleration_data, temporal=True, plot_type=Data2DGraph.LINE_PLOT)

        self.status_bar.showMessage('Created replay cursor acceleration graph. Check graphs tab.')
    

    def create_cursor_jerk_graph(self, replay_data):
        self.status_bar.showMessage('Creating replay cursor jerk graph')

        jerk_data = StdReplayMetrics.cursor_jerk(replay_data)
        self.add_graph_2d_data('replay cursor jerk', jerk_data, temporal=True, plot_type=Data2DGraph.LINE_PLOT)

        self.status_bar.showMessage('Created replay cursor jerk graph. Check graphs tab.')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex  = MainWindow()
    sys.exit(app.exec_())