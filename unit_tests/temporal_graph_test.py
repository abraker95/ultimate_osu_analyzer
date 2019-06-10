import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.data_2d_temporal_graph import Data2DTemporalGraph
from gui.objects.graph.line_plot import LinePlot


class TemporalGraphTest(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        
        self.temporal_graph = Data2DTemporalGraph('Test', ([0], [0]))
        self.setCentralWidget(self.temporal_graph)

        self.setWindowTitle('Graph manager test')
        self.show()


    def time_minupilation_test(self, app):
        print('time_minupilation_test')
        for t in range(1, 2000, 10):
            self.temporal_graph.timeline_marker.setValue(t)
            time.sleep(0.01)
            app.processEvents()