from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from pyqtgraph.dockarea import *

from gui.objects.graph.graphs.tapping_intervals_graph import TappingIntervalsGraph
from gui.objects.graph.graphs.velocity_graph import VelocityGraph
from gui.objects.graph.graphs.rhythmic_complexity_graph import RhythmicComplexityGraph



class AnalysisControls(QWidget):

    def __init__(self):
        super().__init__()

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout    = QVBoxLayout()
        self.dock_area = DockArea()
        self.label     = QLabel('Analysis Controls', self)
        
        # TODO: List of dockable widgets
        self.graphs = [ 
            TappingIntervalsGraph(), 
            VelocityGraph()
        ]


    def construct_gui(self):
        self.setLayout(self.layout)

        # TODO: Handle closing of floating docks
        for graph in self.graphs:
            dock = Dock(graph.getPlotItem().titleLabel.text, size=(1, 1))    # TODO: , closable=True
            dock.addWidget(graph)
            self.dock_area.addDock(dock, 'bottom')

        self.layout.addWidget(self.dock_area)
        self.layout.addWidget(self.label)


    def update_gui(self):
        self.label.setAlignment(Qt.AlignCenter)