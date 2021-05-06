import unittest
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback

from osu.local.replay.replayIO import ReplayIO
from osu.local.beatmap.beatmapIO import BeatmapIO

from gui.objects.layer.layers.std.hitobject_outline_layer import HitobjectOutlineLayer
from gui.objects.layer.layers.std.hitobject_aimpoint_layer import HitobjectAimpointLayer
from gui.objects.layer.layers.std_data_2d_layer import StdData2DLayer

from analysis.osu.std.replay_data import StdReplayData
from analysis.osu.std.std_layers import StdLayers

from generic.switcher import Switcher
from gui.objects.display import Display
from gui.objects.layer.layer_manager import LayerManager



class TestStdReplayVisualization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
        cls.win = QMainWindow()
        
        cls.display = Display()
        cls.display.setFocusPolicy(Qt.NoFocus)

        cls.switcher = Switcher()
        cls.switcher.switch.connect(cls.display.setScene)

        cls.win.setCentralWidget(cls.display)
        cls.win.setWindowTitle('Replay Test')
        cls.win.setGeometry(0, 0, cls.display.width(), cls.display.height())
        cls.win.show()


    def test_browse(self):
        @callback
        def time_browse():
            for t in range(0, 40000, 10):
                time_browse.emit(t)
                self.app.processEvents() 

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\playable\\Within Temptation - The Unforgiving (Armin) [Marathon].osu')
        replay  = ReplayIO.open_replay('unit_tests\\replays\\osu\\Toy - Within Temptation - The Unforgiving [Marathon] (2018-02-06) Osu.osr')

        replay_data = StdReplayData.get_replay_data(replay.play_data)

        layer_manager = LayerManager()
        layer_manager.add_layer('Hitobject outline', HitobjectOutlineLayer(beatmap, time_browse))
        layer_manager.add_layer('Replays', StdData2DLayer('Replay cursor', replay_data, StdLayers.StdReplayCursorLayer, time_browse))

        self.display.setScene(layer_manager)
        time_browse()


    def test_map_switching(self):
        @callback
        def time_browse():
            for t in range(1000, 10000, 10):
                time_browse.emit(t)

                # Switch between map1 and map2 as time ticks
                if t % 1000 <= 500:
                    self.switcher.switch('map_2')
                    self.switcher.get().update_layers()
                else:
                    self.switcher.switch('map_1')
                    self.switcher.get().update_layers()

                self.app.processEvents() 
                time.sleep(.01)

        # Let's have one map have one set of layers, and another map have another set of layers
        layer_manager_1 = LayerManager()
        layer_manager_2 = LayerManager()

        self.switcher.add('map_1', layer_manager_1)
        self.switcher.add('map_2', layer_manager_2)

        beatmap_1 = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\playable\\Mutsuhiko Izumi - Red Goose (nold_1702) [ERT Basic].osu')
        beatmap_2 = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\playable\\Within Temptation - The Unforgiving (Armin) [Marathon].osu')

        layer_manager_1.add_layer('beatmap', HitobjectOutlineLayer(beatmap_1, time_browse))
        layer_manager_1.add_layer('beatmap', HitobjectOutlineLayer(beatmap_2, time_browse))

        layer_manager_2.add_layer('aimpoint', HitobjectAimpointLayer(beatmap_2, time_browse))

        self.switcher.switch.connect(lambda old, new: self.display.setScene(new), inst=self.switcher)
        self.switcher.switch('map_1')

        time_browse()