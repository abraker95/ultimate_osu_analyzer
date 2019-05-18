from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MetricManager(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout = QVBoxLayout()
        self.label  = QLabel('Metric Manager')


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)


    def update_gui(self):
        self.label.setAlignment(Qt.AlignCenter)