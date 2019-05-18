import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.frames.main_frame import MainFrame

from gui.widgets.temporal_hitobject_graph import TemporalHitobjectGraph
from gui.objects.graph.line_plot import LinePlot
from gui.objects.display import Display

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.beatmap.beatmap import Beatmap

from core.gamemode_manager import gamemode_manager
from core.layer_manager import LayerManager

from gui.objects.layer.layers.std.hitobject_outline_layer import HitobjectOutlineLayer
from gui.objects.layer.layers.std.hitobject_aimpoint_layer import HitobjectAimpointLayer

from gui.objects.layer.layers.mania.hitobject_render_layer import HitobjectRenderLayer

#from analysis.map_data_proxy import MapDataProxy
#from analysis.metrics.metric_library_proxy import MetricLibraryProxy
#from analysis.metrics.metric import Metric
#from analysis.osu.std.map_metrics import MapMetrics



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

        self.view_menu              = self.menubar.addMenu('&View')
        self.graphs_menu            = self.view_menu.addMenu('&Graphs')
        self.view_velocity          = QAction("&velocity", self)
        self.view_tapping_intervals = QAction("&tapping intervals", self)
        
        self.toolbar    = self.addToolBar('Exit')
        self.status_bar = self.statusBar()

        self.timeline                 = self.main_frame.bottom_frame.timeline
        self.graph_manager            = self.main_frame.center_frame.right_frame.graph_manager
        self.analysis_controls        = self.main_frame.center_frame.right_frame.analysis_controls
        self.layer_manager_switch_gui = self.main_frame.center_frame.right_frame.layer_manager_switch
        self.map_manager              = self.main_frame.center_frame.mid_frame.map_manager
        self.display                  = self.main_frame.center_frame.mid_frame.display


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

        self.view_velocity.setCheckable(True)
        self.view_velocity.triggered.connect(self.view_velocity_action)

        self.view_tapping_intervals.setCheckable(True)
        self.view_tapping_intervals.triggered.connect(self.view_tapping_intervals_action)

        self.analysis_controls.create_graph_event.connect(self.graph_manager.add_graph)
        self.map_manager.map_changed_event.connect(self.change_map)
        self.map_manager.map_close_event.connect(self.close_map)

        # Allows to forward signals from any temporal graph without having means to get the instance
        TemporalHitobjectGraph.__init__.connect(self.temporal_graph_creation_event)
        TemporalHitobjectGraph.__del__.connect(self.temporal_graph_deletion_event)

        self.layer_manager_switch_gui.switch.connect(lambda old, new: self.display.setScene(new), inst=self.layer_manager_switch_gui)
        self.layer_manager_switch_gui.switch.connect(self.layer_manager_switch_gui.switch_layer_manager, inst=self.layer_manager_switch_gui)

        # gamemode_manger.switch.connect(self.)    # puts out MetricManager


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
            beatmap = BeatmapIO.load_beatmap(beatmap_filename)
            self.map_manager.add_map(beatmap, beatmap.metadata.name)

            self.layer_manager_switch_gui.add(beatmap.metadata.name, LayerManager())
            self.layer_manager_switch_gui.switch(beatmap.metadata.name)

            # TODO: Adding layers will be one of things analysis manager does
            if beatmap.gamemode == Beatmap.GAMEMODE_OSU:
                self.layer_manager_switch_gui.get().add_layer('hitobjects', HitobjectOutlineLayer(beatmap, self.timeline.time_changed_event))
                self.layer_manager_switch_gui.get().add_layer('aimpoints', HitobjectAimpointLayer(beatmap, self.timeline.time_changed_event))

            if beatmap.gamemode == Beatmap.GAMEMODE_MANIA:
                self.layer_manager_switch_gui.get().add_layer('hitobjects', HitobjectRenderLayer(beatmap, self.timeline.time_changed_event))

    def close_map(self, beatmap):
        self.layer_manager_switch_gui.rmv(beatmap.metadata.name)


    def get_osu_files(self, file_type):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters([ file_type ])
        file_dialog.selectNameFilter(file_type)
        
        if file_dialog.exec_():
            return file_dialog.selectedFiles()


    def change_map(self, beatmap):
        if not beatmap: return

        #MapDataProxy.full_hitobject_data.set_data_hitobjects(beatmap.hitobjects)

        # TODO: Fix bug where changing from a new loaded map first time doesn't safe timeline data
        try: self.timeline.save()
        except: pass

        try: self.timeline.load(beatmap.metadata.name)
        except ValueError:
            # Get new timeline range
            min_time, max_time = beatmap.get_time_range()
            self.timeline.setRange(xRange=(min_time - 100, max_time + 100))
            self.timeline.timeline_marker.setValue(min_time)
            self.timeline.save(beatmap.metadata.name)

        #self.timeline.set_hitobject_data(MapDataProxy.full_hitobject_data)

        #self.graph_manager.update_data()

        gamemode_manager.switch(beatmap.gamemode)
        self.layer_manager_switch_gui.switch(beatmap.metadata.name)


    def switch_gamemode(self, gamemode):
        MapDataProxy.set_gamemode(gamemode)
        MetricLibraryProxy.proxy.set_gamemode(gamemode)
        
        '''
        # TODO:
            reset layers to gamemode
            reset analysis to gamemode
        '''

        metric_library = MetricLibraryProxy.proxy.get()
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