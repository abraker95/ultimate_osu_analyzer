from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.objects.playfield_mgr import PlayfieldManager
from misc.callback import callback



class MidFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout            = QHBoxLayout()
        self.playfield_manager = PlayfieldManager()


    def construct_gui(self):
        self.setLayout(self.layout)
        
        self.playfield_manager.currentChanged.connect(self.tab_changed_event)
        self.playfield_manager.tabCloseRequested.connect(self.tab_closing)
        self.layout.addWidget(self.playfield_manager)

        # TODO: label showing cursor pos
        # TODO: label showing pos of selected object


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.playfield_manager.setMovable(True)
        self.playfield_manager.setTabsClosable(True)

    
    def add_tab(self, playfield, name):
        self.playfield_manager.addTab(playfield, name)
        self.playfield_manager.setCurrentIndex(self.playfield_manager.indexOf(playfield))


    @callback
    def tab_changed_event(self, idx):
        print('Tab changed to index ', idx)
        self.tab_changed_event.emit(self.playfield_manager.widget(idx))


    @callback
    def tab_closing(self, idx):
        print('TODO: tab implement closing')