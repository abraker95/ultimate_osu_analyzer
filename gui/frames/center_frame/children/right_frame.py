from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class RightFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout = QHBoxLayout()
        self.label  = QLabel("RightFrame", self)

        # TODO: Vertical layout
        # TODO: List of dockable widgets


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.label.setAlignment(Qt.AlignCenter)