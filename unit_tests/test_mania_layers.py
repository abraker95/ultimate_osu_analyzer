import unittest
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback

from osu.local.replay.replayIO import ReplayIO
from osu.local.beatmap.beatmapIO import BeatmapIO

from analysis.osu.mania.action_data import ManiaActionData
from analysis.osu.mania.map_metrics import ManiaMapMetrics

from gui.objects.layer.layers.mania_data_2d_layer import ManiaData2DLayer
from analysis.osu.mania.mania_layers import ManiaLayers

from gui.objects.display import Display
from gui.objects.layer.layer_manager import LayerManager



class TestManiaLayers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
        cls.win = QMainWindow()
        
        cls.display = Display()
        cls.display.setFocusPolicy(Qt.NoFocus)

        cls.win.setCentralWidget(cls.display)
        cls.win.setWindowTitle('Mania Layers Test')
        cls.win.setGeometry(0, 0, cls.display.width(), cls.display.height())
        cls.win.show()


    def test_action_fill_layer(self):
        @callback
        def time_browse():
            for t in range(8000, 12000, 10):
                time_browse.emit(t)
                self.app.processEvents() 

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\playable\\DJ Genericname - Dear You (Taiwan-NAK) [S.Star\'s 4K HD+].osu')
        replay  = ReplayIO.open_replay('unit_tests\\replays\\mania\\abraker - DJ Genericname - Dear You [S.Star\'s 4K HD+] (2020-04-25) OsuMania.osr')

        map_data = ManiaActionData.get_map_data(beatmap.hitobjects)
        replay_data = ManiaActionData.get_replay_data(replay.play_data, beatmap.difficulty.cs)

        map_layer = ManiaData2DLayer('Map Layer', map_data, ManiaLayers.ManiaActionFillLayer, time_browse, color=(255, 0, 0, 255))
        replay_layer = ManiaData2DLayer('Replay layer', replay_data, ManiaLayers.ManiaActionFillLayer, time_browse)

        layer_manager = LayerManager()
        layer_manager.add_layer('Layers', map_layer)
        layer_manager.add_layer('Layers', replay_layer)

        self.display.setScene(layer_manager)
        time_browse()


    def test_action_layer(self):
        @callback
        def time_browse():
            for t in range(18000, 24000, 3):
                time_browse.emit(t)
                self.app.processEvents() 

        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\playable\\DJ Genericname - Dear You (Taiwan-NAK) [S.Star\'s 4K HD+].osu')
        map_data = ManiaActionData.get_map_data(beatmap.hitobjects)
        data_layer = ManiaData2DLayer('Detection Layer', map_data, ManiaLayers.ManiaActionLayer, time_browse)

        layer_manager = LayerManager()
        layer_manager.add_layer('Layers', data_layer)

        self.display.setScene(layer_manager)
        time_browse()