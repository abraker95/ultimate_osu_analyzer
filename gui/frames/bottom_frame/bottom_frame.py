from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.timeline import Timeline


class BottomFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout   = QHBoxLayout()
        self.label    = QLabel("BottomFrame", self)
        self.timeline = Timeline()

        # TODO: Horizontal layer
        # TODO: label frame
        # TODO: graph frame
        # TODO: ctrl frame

    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.timeline)


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.label.setAlignment(Qt.AlignCenter)