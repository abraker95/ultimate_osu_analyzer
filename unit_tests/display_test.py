import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback
from osu.local.beatmap.beatmapIO import BeatmapIO

from gui.objects.layer.layers.std.hitobject_outline_layer import HitobjectOutlineLayer
from gui.objects.layer.layers.std.hitobject_aimpoint_layer import HitobjectAimpointLayer

from generic.switcher import Switcher
from gui.objects.scene import Scene
from gui.objects.display import Display
from gui.objects.layer.layer_manager import LayerManager


class DisplayTest(QMainWindow):

    title = 'Display Test'
    left   = 100
    top    = 100
    width  = 1080
    height = 720

    def __init__(self, app, beatmap_filepath):
        QMainWindow.__init__(self)

        self.display = Display()
        self.display.setFocusPolicy(Qt.NoFocus)

        self.switcher = Switcher()
        self.switcher.switch.connect(self.display.setScene)

        self.setCentralWidget(self.display)
        self.setWindowTitle(DisplayTest.title)
        self.setGeometry(0, 0, self.display.width(), self.display.height())
        self.show()

        self.switcher_test()
        self.time_browse_test(app)


    def switcher_test(self):
        self.layer_manager_1 = LayerManager()
        self.layer_manager_2 = LayerManager()

        self.switcher.add('map_1', self.layer_manager_1)
        self.switcher.add('map_2', self.layer_manager_2)

        self.beatmap_1 = BeatmapIO.load_beatmap('unit_tests\\maps\\Mutsuhiko Izumi - Red Goose (nold_1702) [ERT Basic].osu')
        self.beatmap_2 = BeatmapIO.load_beatmap('unit_tests\\maps\\Within Temptation - The Unforgiving (Armin) [Marathon].osu')

        self.layer_manager_1.add_layer('beatmap', HitobjectOutlineLayer(self.beatmap_1, self.time_browse_test))
        self.layer_manager_1.add_layer('beatmap', HitobjectOutlineLayer(self.beatmap_2, self.time_browse_test))

        self.layer_manager_2.add_layer('aimpoint', HitobjectAimpointLayer(self.beatmap_2, self.time_browse_test))

        self.switcher.switch('map_1')
        self.switcher.get().update_layers()
        
    '''
    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            self.display.set_time(self.display.time - 50)

        if key == Qt.Key_Right:
            self.display.set_time(self.display.time + 50)
    '''

    @callback
    def time_browse_test(self, app):
        print('time_browse_test')
        for t in range(0, 50000, 1000):
            self.time_browse_test.emit(t)

            if t > 25000:
                self.switcher.switch('map_2')
                self.switcher.get().update_layers()

            app.processEvents() 
            time.sleep(.1)


    def layer_toggle_test(self):
        print('layer_toggle_test')
        # TODO: toggle layers