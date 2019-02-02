from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .children.left_frame import LeftFrame
from .children.mid_frame import MidFrame
from .children.right_frame import RightFrame



class CenterFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout      = QVBoxLayout()
        self.splitter    = QSplitter(Qt.Horizontal)
        self.left_frame  = LeftFrame()
        self.mid_frame   = MidFrame()
        self.right_frame = RightFrame()


    def construct_gui(self):
        self.setLayout(self.layout)

        self.layout.addWidget(self.splitter)
        self.splitter.addWidget(self.left_frame)
        self.splitter.addWidget(self.mid_frame)
        self.splitter.addWidget(self.right_frame)


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.splitter.setSizes([ self.width()/12, self.width()/3,  self.width()/12 ])