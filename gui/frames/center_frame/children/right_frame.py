from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.manager_switch import ManagerSwitch
from gui.widgets.analysis_controls import AnalysisControls
from gui.widgets.metric_manager import MetricManager
from gui.widgets.ipython_console import IPythonConsole


class RightFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout    = QHBoxLayout()
        self.tabs_area = QTabWidget()

        self.layer_manager_switch  = ManagerSwitch()
        self.replay_manager_switch = ManagerSwitch()
        self.graph_manager_switch  = ManagerSwitch()
        self.analysis_controls     = AnalysisControls()
        self.metric_manager        = MetricManager()
        self.ipython_console       = IPythonConsole()


    def construct_gui(self):
        self.setLayout(self.layout)

        self.tabs_area.addTab(self.layer_manager_switch, 'Layers')
        self.tabs_area.addTab(self.replay_manager_switch, 'Replays')
        self.tabs_area.addTab(self.graph_manager_switch, 'Graphs')
        self.tabs_area.addTab(self.analysis_controls, 'Analysis')
        self.tabs_area.addTab(self.metric_manager, 'Metrics')
        self.tabs_area.addTab(self.ipython_console, 'Console')
        self.layout.addWidget(self.tabs_area)


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)

        