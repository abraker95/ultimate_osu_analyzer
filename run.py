import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.frames.main_frame import MainFrame

from gui.widgets.temporal_hitobject_graph import TemporalHitobjectGraph
from gui.objects.graph.line_plot import LinePlot

from osu.local.playfield import Playfield
from osu.local.beatmap.beatmap import Beatmap

from analysis.map_data_proxy import MapDataProxy
from analysis.metrics.metric_library_proxy import MetricLibraryProxy
from analysis.metrics.metric import Metric
from analysis.osu.std.map_metrics import MapMetrics



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
        self.close_action        = QAction("&Quit w", self)
        
        self.toolbar    = self.addToolBar('Exit')
        self.status_bar = self.statusBar()

        self.timeline            = self.main_frame.bottom_frame.timeline
        self.graph_manager       = self.main_frame.center_frame.right_frame.graph_manager
        self.analysis_controls   = self.main_frame.center_frame.right_frame.analysis_controls
        self.layer_manager_stack = self.main_frame.center_frame.right_frame.layer_manager_stack


    def construct_gui(self):
        self.setCentralWidget(self.main_frame)
        self.toolbar.addAction(QAction(QIcon('new.bmp'), 'test menubar button', self))

        self.file_menu.addAction(self.open_beatmap_action)
        self.file_menu.addAction(self.close_action)
        
        self.open_beatmap_action.setStatusTip('Open *.osu beatmap for analysis')
        self.open_beatmap_action.setShortcut('Ctrl+N')
        self.open_beatmap_action.triggered.connect(self.open_beatmap)

        self.close_action.setStatusTip('Quit the application')
        self.close_action.setShortcut('Ctrl+Q')
        self.close_action.triggered.connect(self.close_application)


        self.analysis_controls.create_graph_event.connect(self.graph_manager.add_graph)
        self.main_frame.center_frame.mid_frame.tab_changed_event.connect(self.change_playfield)

        # Allows to forward signals from any temporal graph without having means to get the instance
        TemporalHitobjectGraph.__init__.connect(self.temporal_graph_creation_event)
        TemporalHitobjectGraph.__del__.connect(self.temporal_graph_deletion_event)


    def update_gui(self):
        self.setWindowTitle(MainWindow.title)
        self.setGeometry(MainWindow.left, MainWindow.top, MainWindow.width, MainWindow.height)
        self.status_bar.showMessage('Statusbar test message')
        self.show()


    def temporal_graph_creation_event(self, graph):
        # Since everything connects to the timeline, and the timeline is always existing,
        # it acts as a central updater for every other temporal graph
        self.timeline.time_changed_event.connect(graph.timeline_marker.setValue)
        graph.time_changed_event.connect(self.timeline.timeline_marker.setValue)


    def temporal_graph_deletion_event(self, graph):
        self.timeline.time_changed_event.disconnect(graph.timeline_marker.setValue)
        graph.time_changed_event.disconnect(self.timeline.timeline_marker.setValue)


    def open_beatmap(self):
        beatmap_filenames = self.get_osu_files('osu files (*.osu)')
        if not beatmap_filenames: return

        for beatmap_filename in beatmap_filenames:
            print(beatmap_filename)

            # Create a new playfield and load the beatmap into it
            playfield = Playfield()
            playfield.setFocusPolicy(Qt.NoFocus)
            playfield.load_beatmap(Beatmap(beatmap_filename))

            # TODO: Currently the lables are based off map's full name
            #       That's fine, but if the same map is opened multiple times, especially after being edited,
            #       the layers refer to each other under the same map's name and will apply to all maps named with same name
            #       Use an MD5 hash instead
            map_name = playfield.beatmap.metadata.name

            # Establish connection between the timeline and playfield's time setting
            self.timeline.time_changed_event.connect(playfield.set_time)
            
            # Add new layer controls area for controlling displayed map layers
            self.layer_manager_stack.add_layer_manager(map_name)

            # Establish a connection between the created layer manager and playfield's add layer and layer manager's remove layer events
            layer_manager = self.layer_manager_stack.get_layer_manager(map_name)
            playfield.add_layer_event.connect(layer_manager.add_layer)
            
            layer_manager.remove_layer_event.connect(playfield.remove_layer)
            layer_manager.layer_change_event.connect(playfield.layer_changed)

            # Add new tab to display playfield; 
            # Note: this has to go last to be able to switch to created layer manager
            self.main_frame.center_frame.mid_frame.add_tab(playfield, map_name)

            # Populate layer manager with plafield layers
            playfield.create_basic_map_layers()


    def get_osu_files(self, file_type):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters([ file_type ])
        file_dialog.selectNameFilter(file_type)
        
        if file_dialog.exec_():
            return file_dialog.selectedFiles()


    def change_playfield(self, playfield):
        self.switch_gamemode(playfield.beatmap.gamemode)
        MapDataProxy.full_hitobject_data.set_data_hitobjects(playfield.beatmap.hitobjects)

        # Update timeline range
        min_time, max_time = playfield.beatmap.get_time_range()
        self.timeline.setRange(xRange=(min_time - 100, max_time + 100))
        self.timeline.set_hitobject_data(MapDataProxy.full_hitobject_data)

        # Change to the layer manager responsible for the playfield now displayed
        map_name = playfield.beatmap.metadata.name
        layer_manager_stack = self.main_frame.center_frame.right_frame.layer_manager_stack
        layer_manager_stack.set_layer_manager_active(map_name)

        self.graph_manager.update_data()

        print('\tTODO: save timeline marker position')
        print('\tTODO: update statistics on the right side')


    def switch_gamemode(self, gamemode):
        MapDataProxy.set_gamemode(gamemode)
        MetricLibraryProxy.proxy.set_gamemode(gamemode)
        
        '''
        # TODO:
            reset layers to gamemode
            reset analysis to gamemode
        '''

        metric_library = MetricLibraryProxy.proxy.get_active_lib()
        print('Available metrics: ' + str(metric_library.get_names()))

        analysis_controls = self.main_frame.center_frame.right_frame.analysis_controls
        analysis_controls.refresh_metrics()

        if gamemode == Beatmap.GAMEMODE_OSU:
            print('Gamemode is now osu')
            

            graph_manager = self.main_frame.center_frame.right_frame.graph_manager
            self.graph_manager.clear()

            self.graph_manager.add_graph(TemporalHitobjectGraph(LinePlot(), 'Tapping Intervals',   MapMetrics.calc_tapping_intervals))
            self.graph_manager.add_graph(TemporalHitobjectGraph(LinePlot(), 'Velocity',            MapMetrics.calc_velocity))
            self.graph_manager.add_graph(TemporalHitobjectGraph(LinePlot(), 'Rhythmic Complexity', MapMetrics.calc_rhythmic_complexity))

            # TODO: Enable velocity
            # TODO: Enable acceleration
            pass

        if gamemode == Beatmap.GAMEMODE_MANIA:
            print('Gamemode is now mania')
            self.graph_manager.clear()


        if gamemode == Beatmap.GAMEMODE_TAIKO:
            print('Gamemode is now taiko')
            self.graph_manager.clear()

        if gamemode == Beatmap.GAMEMODE_CATCH:
            print('Gamemode is now catch')
            self.graph_manager.clear()


    def close_application(self):
        sys.exit()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex  = MainWindow()
    sys.exit(app.exec_())