from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback



class MidFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout    = QHBoxLayout()
        self.tabs_area = QTabWidget()
        self.tabs      = []

        self.label1  = QLabel("Map 1", self)
        self.label2  = QLabel("Map 2", self)


    def construct_gui(self):
        self.setLayout(self.layout)
        
        self.tabs_area.addTab(self.label1, "Test tab 2")
        self.tabs_area.addTab(self.label2, "Test tab 2")
        self.tabs_area.currentChanged.connect(self.tabs_changed)
        self.layout.addWidget(self.tabs_area)

        # TODO: play area
        # TODO: label showing cursor pos
        # TODO: label showing pos of selected object


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)


    def add_tab(self, playfield, name):
        self.tabs.append(playfield)
        self.tabs_area.addTab(playfield, name)


    @callback
    def tabs_changed(self, idx):
        print('Tab changed to index ', idx)
        self.tabs_changed.emit(self.tabs[idx])