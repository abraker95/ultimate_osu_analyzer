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
        self.layout     = QHBoxLayout()
        self.tabs_area  = QTabWidget()


    def construct_gui(self):
        self.setLayout(self.layout)
        
        self.tabs_area.currentChanged.connect(self.tab_changed)
        self.tabs_area.tabCloseRequested.connect(self.tab_closing)
        self.layout.addWidget(self.tabs_area)

        # TODO: play area
        # TODO: label showing cursor pos
        # TODO: label showing pos of selected object


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.tabs_area.setMovable(True)
        self.tabs_area.setTabsClosable(True)


    def get_current_playfield(self):
        return self.tabs_area.widget(self.tabs_area.currentIndex())


    def add_tab(self, playfield, name):
        self.tabs_area.addTab(playfield, name)
        self.tabs_area.setCurrentIndex(self.tabs_area.indexOf(playfield))


    @callback
    def tab_changed(self, idx):
        print('Tab changed to index ', idx)
        self.tab_changed.emit(self.tabs_area.widget(idx))


    @callback
    def tab_closing(self, idx):
        print('TODO: tab implement closing')