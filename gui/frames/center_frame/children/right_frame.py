from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.layer_manager_stack import LayerManagerStack
from gui.widgets.analysis_controls import AnalysisControls


class RightFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout    = QHBoxLayout()
        self.tabs_area = QTabWidget()

        self.layer_manager_stack = LayerManagerStack()
        self.analysis_controls   = AnalysisControls()


    def construct_gui(self):
        self.setLayout(self.layout)

        self.tabs_area.addTab(self.layer_manager_stack, 'Layers')
        self.tabs_area.addTab(self.analysis_controls, 'Analysis')
        self.layout.addWidget(self.tabs_area)


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)