from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback

from osu.local.replay.replayIO import ReplayIO
from osu.local.beatmap.beatmapIO import BeatmapIO

from gui.objects.layer.layers.std.hitobject_outline_layer import HitobjectOutlineLayer
from gui.objects.layer.layers.std.replay_cursor_layer import StdReplayCursorLayer

from gui.objects.scene import Scene
from gui.objects.display import Display
from gui.objects.layer.layer_manager import LayerManager


class StdReplayTest(QMainWindow):

    title = 'Replay Test'
    left   = 100
    top    = 100
    width  = 1080
    height = 720

    def __init__(self, app):
        QMainWindow.__init__(self)

        self.display = Display()
        self.display.setFocusPolicy(Qt.NoFocus)

        self.beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\Within Temptation - The Unforgiving (Armin) [Marathon].osu')
        self.replay  = ReplayIO.open_replay('unit_tests\\replays\\Toy - Within Temptation - The Unforgiving [Marathon] (2018-02-06) Osu.osr')

        self.layer_manager = LayerManager()
        self.layer_manager.add_layer('Hitobject outline', HitobjectOutlineLayer(self.beatmap, self.time_browse_test))
        self.layer_manager.add_layer('Replay cursor', StdReplayCursorLayer(self.replay, self.time_browse_test))

        self.display.setScene(self.layer_manager)

        self.setCentralWidget(self.display)
        self.setWindowTitle(StdReplayTest.title)
        self.setGeometry(0, 0, self.display.width(), self.display.height())
        self.show()

        self.time_browse_test(app)
    
 
    @callback
    def time_browse_test(self, app):
        print('time_browse_test')
        for t in range(0, 40000, 10):
            self.time_browse_test.emit(t)
            app.processEvents() 