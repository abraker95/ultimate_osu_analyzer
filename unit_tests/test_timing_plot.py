import unittest
import pyqtgraph

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import time
import numpy as np

from gui.objects.graph.timing_plot import TimingPlot



class TestTimingPlot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):       
        cls.app = QApplication([])

        cls.ts = np.arange(30)
        cls.te = np.arange(30) + 10
        cls.c = [ (200, x*5, 100, 100) for x in range(30) ]


    def test_timing_plot(self):
        plot = pyqtgraph.plot()
        plot.addItem(TimingPlot(self.ts, self.te))
        plot.show()