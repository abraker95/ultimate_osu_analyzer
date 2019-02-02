from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class MidFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout = QHBoxLayout()
        self.label  = QLabel("MidFrame", self)


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)        # TODO: Replace with tabbed widget and create a inner mid frame

        # TODO: play area
        # TODO: label showing cursor pos
        # TODO: label showing pos of selected object


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.label.setAlignment(Qt.AlignCenter)