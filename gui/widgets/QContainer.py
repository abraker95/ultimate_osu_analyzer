from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class QContainer(QWidget):

    def __init__(self, layout):
        QWidget.__init__(self)

        self.layout = layout
        self.setLayout(self.layout)


    def addWidget(self, widget):
        self.layout.addWidget(widget)


    def rmvWidget(self, widget):
        self.layout.removeWidget(widget)


    def get(self):
        return self.layout