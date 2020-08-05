import unittest

import time
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.data_2d_temporal_graph import Data2DTemporalGraph
from gui.objects.graph.line_plot import LinePlot



class TestGraph(unittest.TestCase):

    @classmethod
    def setUpClass(cls):       
        cls.app = QApplication([])

        cls.data_x = np.arange(30)
        cls.data_y = np.sin(cls.data_x/4)


    def test_scatter_plot(self):
        temporal_graph = Data2DTemporalGraph('Test', None, plot_type=Data2DTemporalGraph.SCATTER_PLOT)
        temporal_graph.show()

        for t in range(0, 30*10, 1):
            self.data_y = np.sin(self.data_x/4 + t/10)

            temporal_graph.timeline_marker.setValue(t/10)
            temporal_graph.update_data((self.data_x, self.data_y))

            time.sleep(0.01)
            self.app.processEvents()


    def test_line_plot(self):
        temporal_graph = Data2DTemporalGraph('Test', None, plot_type=Data2DTemporalGraph.LINE_PLOT)
        temporal_graph.show()

        for t in range(0, 30*10, 1):
            self.data_y = np.sin(self.data_x/4 + t/10)

            temporal_graph.timeline_marker.setValue(t/10)
            temporal_graph.update_data((self.data_x, self.data_y))

            time.sleep(0.01)
            self.app.processEvents()


    def test_bar_plot(self):
        temporal_graph = Data2DTemporalGraph('Test', None, plot_type=Data2DTemporalGraph.BAR_PLOT)
        temporal_graph.show()

        for t in range(0, 30*10, 1):
            self.data_y = np.sin(self.data_x/4 + t/10)

            temporal_graph.timeline_marker.setValue(t/10)
            temporal_graph.update_data((10, self.data_y))

            time.sleep(0.01)
            self.app.processEvents()


    def test_graph_data(self):
        # TODO: Test whether infinities get filtered
        pass