from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback

from osu.local.replay import Replay
from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.beatmap.beatmap_utility import BeatmapUtil

from gui.objects.layer.layers.std.hitobject_outline_layer import HitobjectOutlineLayer
from gui.objects.layer.layers.std.replay_layer import ReplayLayer

from gui.objects.scene import Scene
from gui.objects.display import Display
from gui.objects.layer.layer_manager import LayerManager


class ReplayTest(QMainWindow):

    title = 'Replay Test'
    left   = 100
    top    = 100
    width  = 1080
    height = 720

    def __init__(self, app):
        QMainWindow.__init__(self)

        self.display = Display()
        self.display.setFocusPolicy(Qt.NoFocus)

        self.beatmap = BeatmapIO.load_beatmap('unit_tests\\maps\\Within Temptation - The Unforgiving (Armin) [Marathon].osu')
        self.replay  = Replay('unit_tests\\replays\\Toy - Within Temptation - The Unforgiving [Marathon] (2018-02-06) Osu.osr')

        self.layer_manager = LayerManager()
        self.layer_manager.add_layer('beatmap', HitobjectOutlineLayer(self.beatmap, self.time_browse_test))
        self.layer_manager.add_layer('replay',  ReplayLayer(self.replay, self.time_browse_test))

        self.display.setScene(self.layer_manager)

        self.setCentralWidget(self.display)
        self.setWindowTitle(ReplayTest.title)
        self.setGeometry(0, 0, self.display.width(), self.display.height())
        self.show()

        self.time_browse_test(app)
    
 
    @callback
    def time_browse_test(self, app):
        print('time_browse_test')
        for t in range(0, 50000, 10):
            self.time_browse_test.emit(t)
            app.processEvents() 