from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class Layer(QGraphicsItem):


    def __init__(self, name):
        QGraphicsItem.__init__(self)

        self.name    = name
        self.ratio_x = 1.0
        self.ratio_y = 1.0


    def area_resize_event(self, width, height):
        raise NotImplementedError()


    def set_layer_opacity(self, opacity):
        self.setOpacity(opacity)


    def set_layer_enable(self, enable):
        self.setVisible(enable)