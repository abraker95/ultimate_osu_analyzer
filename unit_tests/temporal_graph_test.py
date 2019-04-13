import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.temporal_hitobject_graph import TemporalHitobjectGraph
from gui.objects.graph.line_plot import LinePlot

from analysis.osu.std.map_metrics import MapMetrics


class TemporalGraphTest(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        
        self.temporal_graph = TemporalHitobjectGraph(LinePlot(), 'Test', lambda: None)
        self.setCentralWidget(self.temporal_graph)

        self.setWindowTitle('Graph manager test')
        self.show()


    def time_minupilation_test(self, app):
        print('time_minupilation_test')
        for t in range(1, 2000, 10):
            self.temporal_graph.timeline_marker.setValue(t)
            time.sleep(0.01)
            app.processEvents()