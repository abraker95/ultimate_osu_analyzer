from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from pyqtgraph.dockarea import *

from gui.widgets.temporal_hitobject_graph import TemporalHitobjectGraph
from gui.objects.graph.line_plot import LinePlot
from gui.objects.abstract_state_manager import AbstractStateManager

from analysis.osu.std.map_metrics import MapMetrics


class GraphManager(QWidget):

    def __init__(self):
        super().__init__()

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout    = QVBoxLayout()
        self.dock_area = DockArea()
        
        self.graphs = [ 
            TemporalHitobjectGraph(LinePlot(), 'Tapping Intervals',   MapMetrics.calc_tapping_intervals),
            TemporalHitobjectGraph(LinePlot(), 'Velocity',            MapMetrics.calc_velocity),
            TemporalHitobjectGraph(LinePlot(), 'Rhythmic Complexity', MapMetrics.calc_rhythmic_complexity),
        ]


    def construct_gui(self):
        self.setLayout(self.layout)

        for graph in self.graphs:
            dock = Dock(graph.getPlotItem().titleLabel.text, size=(1, 1))    # TODO: , closable=True
            dock.addWidget(graph)
            self.dock_area.addDock(dock, 'bottom')


        self.layout.addWidget(self.dock_area)


    def update_gui(self):
        pass

