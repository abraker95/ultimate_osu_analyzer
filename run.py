import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.frames.main_frame import MainFrame
from osu.local.playfield import Playfield
from osu.local.beatmap.beatmap import Beatmap

from analysis.map_data_proxy import MapDataProxy


class MainWindow(QMainWindow):

    title = 'Ultimate osu! Analyzer'
    left   = 100
    top    = 100
    width  = 1080
    height = 720

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.main_frame = MainFrame() 
        self.menubar    = self.menuBar()

        self.fileMenu   = self.menubar.addMenu('&File')
        self.open_beatmap_action = QAction("&Open beatmap", self)
        self.close_action        = QAction("&Quit w", self)
        
        self.toolbar    = self.addToolBar('Exit')
        self.status_bar = self.statusBar()


    def construct_gui(self):
        self.setCentralWidget(self.main_frame)
        self.toolbar.addAction(QAction(QIcon('new.bmp'), 'test menubar button', self))

        self.fileMenu.addAction(self.open_beatmap_action)
        self.fileMenu.addAction(self.close_action)
        
        self.open_beatmap_action.setStatusTip('Open *.osu beatmap for analysis')
        self.open_beatmap_action.setShortcut('Ctrl+N')
        self.open_beatmap_action.triggered.connect(self.open_beatmap)

        self.close_action.setStatusTip('Quit the application')
        self.close_action.setShortcut('Ctrl+Q')
        self.close_action.triggered.connect(self.close_application)

        self.main_frame.center_frame.mid_frame.tab_changed_event.connect(self.change_playfield)

        timeline          = self.main_frame.bottom_frame.timeline
        analysis_controls = self.main_frame.center_frame.right_frame.analysis_controls

        for graph in analysis_controls.graphs:
            graph.time_changed_event.connect(timeline.timeline_marker.setValue)
            timeline.time_changed_event.connect(graph.timeline_marker.setValue)


    def update_gui(self):
        self.setWindowTitle(MainWindow.title)
        self.setGeometry(MainWindow.left, MainWindow.top, MainWindow.width, MainWindow.height)
        self.status_bar.showMessage('Statusbar test message')
        self.show()


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
            timeline = self.main_frame.bottom_frame.timeline
            timeline.time_changed_event.connect(playfield.set_time)
            
            # Add new layer controls area for controlling displayed map layers
            layer_manager_stack = self.main_frame.center_frame.right_frame.layer_manager_stack
            layer_manager_stack.add_layer_manager(map_name)

            # Establish a connection between the created layer manager and playfield's add layer and layer manager's remove layer events
            layer_manager = layer_manager_stack.get_layer_manager(map_name)
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
        self.switch_gamode(playfield.beatmap.gamemode)
        MapDataProxy.full_hitobject_data.set_data_hitobjects(playfield.beatmap.hitobjects)

        # Update timeline range
        min_time, max_time = playfield.beatmap.get_time_range()
        timeline = self.main_frame.bottom_frame.timeline
        timeline.setRange(xRange=(min_time - 100, max_time + 100))
        timeline.set_hitobject_data(MapDataProxy.full_hitobject_data)

        # Change to the layer manager responsible for the playfield now displayed
        map_name = playfield.beatmap.metadata.name
        layer_manager_stack = self.main_frame.center_frame.right_frame.layer_manager_stack
        layer_manager_stack.set_layer_manager_active(map_name)

        analysis_controls = self.main_frame.center_frame.right_frame.analysis_controls

        for graph in analysis_controls.graphs:
            graph.update_data()

        print('\tTODO: save timeline marker position')
        print('\tTODO: update statistics on the right side')


    def switch_gamode(self, gamemode):
        MapDataProxy.set_gamemode(gamemode)
        '''
        # TODO:
            reset layers to gamemode
            reset analysis to gamemode
        '''
        pass


    def close_application(self):
        sys.exit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex  = MainWindow()
    sys.exit(app.exec_())