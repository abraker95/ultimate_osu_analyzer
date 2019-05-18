from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.layer_manager_switch import LayerManagerSwitch
from gui.widgets.replay_manager import ReplayManager
from gui.widgets.graph_manager import GraphManager
from gui.widgets.analysis_controls import AnalysisControls
from gui.widgets.metric_manager import MetricManager


class RightFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout    = QHBoxLayout()
        self.tabs_area = QTabWidget()

        self.layer_manager_switch = LayerManagerSwitch()
        self.replay_manager       = ReplayManager()
        self.graph_manager        = GraphManager()
        self.analysis_controls    = AnalysisControls()
        self.metric_manager       = MetricManager()


    def construct_gui(self):
        self.setLayout(self.layout)

        self.tabs_area.addTab(self.layer_manager_switch, 'Layers')
        self.tabs_area.addTab(self.replay_manager, 'Replays')
        self.tabs_area.addTab(self.graph_manager, 'Graphs')
        self.tabs_area.addTab(self.analysis_controls, 'Analysis')
        self.tabs_area.addTab(self.metric_manager, 'Metrics')
        self.layout.addWidget(self.tabs_area)


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)