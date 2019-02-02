from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class LeftFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout = QHBoxLayout()
        self.label  = QLabel("LeftFrame", self)


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)

        # TODO: folder tree/collections view frame
        # TODO: folder tree view button
        # TODO: collections view button


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.label.setAlignment(Qt.AlignCenter)