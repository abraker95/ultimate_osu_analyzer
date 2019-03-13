import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.frames.main_frame import MainFrame
from osu.local.playfield import Playfield
from osu.local.beatmap.beatmap import Beatmap


class MainWindow(QMainWindow):

    title = 'osu! replay analyzer v2.0'
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

        self.main_frame.bottom_frame.timeline.time_changed.connect(self.time_changed_event)

        tab_manager = self.main_frame.center_frame.mid_frame
        tab_manager.tab_changed.connect(self.playfield_change_event)

        layer_controls = self.main_frame.center_frame.right_frame.layer_controls
        layer_controls.layer_change_event.connect(lambda: tab_manager.get_current_playfield().layer_changed())
        layer_controls.remove_layer_event.connect(lambda layer_name: tab_manager.get_current_playfield().remove_layer(layer_name))


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

            playfield = Playfield()
            playfield.setFocusPolicy(Qt.NoFocus)
            playfield.load_beatmap(Beatmap(beatmap_filename))

            playfield.add_layer.connect(self.main_frame.center_frame.right_frame.layer_controls.add_layer)

            map_name = playfield.beatmap.metadata.name
            self.main_frame.center_frame.mid_frame.add_tab(playfield, map_name)


    def get_osu_files(self, file_type):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters([ file_type ])
        file_dialog.selectNameFilter(file_type)
        
        if file_dialog.exec_():
            return file_dialog.selectedFiles()


    def playfield_change_event(self, playfield):
        min_time, max_time = playfield.beatmap.get_time_range()
        self.main_frame.bottom_frame.timeline.setRange(xRange=(min_time - 100, max_time + 100))
        self.main_frame.center_frame.right_frame.layer_controls.create_layer_ctrls_from_layers(playfield.get_layers())
        print('\tTODO: save timeline marker position')
        print('\tTODO: update statistics on the right side')


    def time_changed_event(self, time):
        playfield = self.get_current_playfield()
        if not playfield: return

        playfield.set_time(time)


    def get_current_playfield(self):
        idx = self.main_frame.center_frame.mid_frame.tabs_area.currentIndex()
        return self.main_frame.center_frame.mid_frame.tabs_area.widget(idx)


    def close_application(self):
        sys.exit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex  = MainWindow()
    sys.exit(app.exec_())