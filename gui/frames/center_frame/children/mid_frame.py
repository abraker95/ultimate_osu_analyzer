from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.map_manager import MapManager
from gui.objects.display import Display
from misc.callback import callback



class MidFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout      = QVBoxLayout()
        self.map_manager = MapManager()
        self.display     = Display()


    def construct_gui(self):
        self.setLayout(self.layout)
        
        #self.map_manager.currentChanged.connect(self.map_changed_event)
        #self.map_manager.tabCloseRequested.connect(self.tab_closing)
        
        self.layout.addWidget(self.map_manager)
        self.layout.addWidget(self.display)

        # TODO: label showing cursor pos
        # TODO: label showing pos of selected object


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.map_manager.setMovable(True)
        self.map_manager.setTabsClosable(True)