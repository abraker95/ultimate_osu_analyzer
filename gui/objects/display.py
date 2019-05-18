from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback



class Display(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)

        self.setStyleSheet('background-color: #FEFEFE')
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.scene = None