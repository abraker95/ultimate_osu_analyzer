from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .center_frame.center_frame import CenterFrame
from .bottom_frame.bottom_frame import BottomFrame


class MainFrame(QWidget):
 
    def __init__(self):
        super().__init__()

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout       = QVBoxLayout()
        self.splitter     = QSplitter(Qt.Vertical)
        self.center_frame = CenterFrame()
        self.bottom_frame = BottomFrame()


    def construct_gui(self):
        self.setLayout(self.layout)
        
        self.layout.addWidget(self.splitter)
        self.splitter.addWidget(self.center_frame)
        self.splitter.addWidget(self.bottom_frame)


    def update_gui(self):
        self.splitter.setSizes([ self.height(), self.height()/8 ])