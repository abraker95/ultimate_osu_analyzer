import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.layer_controller import LayerController
from gui.objects.layer.layer import Layer


class LayerControllerTest(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        
        self.layer_controller = LayerController(Layer('test'))
        self.setCentralWidget(self.layer_controller)

        self.setWindowTitle('Layer controller test')
        self.show()


    def visibility_toggle_test(self, app):
        print('visibility_toggle_test')
        # TODO
        pass