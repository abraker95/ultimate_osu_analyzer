from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.objects.graph.graphs.tapping_intervals_graph import TappingIntervalsGraph
from gui.objects.graph.graphs.velocity_graph import VelocityGraph



class AnalysisControls(QWidget):

    def __init__(self):
        super().__init__()

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout = QVBoxLayout()
        self.label  = QLabel('Analysis Controls', self)
        
        # TODO: List of dockable widgets
        self.graphs = [ 
            TappingIntervalsGraph(), 
            VelocityGraph()
        ]


    def construct_gui(self):
        self.setLayout(self.layout)

        for graph in self.graphs:
            self.layout.addWidget(graph)


    def update_gui(self):
        self.label.setAlignment(Qt.AlignCenter)