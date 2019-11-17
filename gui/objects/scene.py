from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Scene(QGraphicsScene):

    def __init__(self):
        QGraphicsScene.__init__(self)


    def add_layer(self, layer):
        print(self, layer)
        self.addItem(layer)
        self.update()

        layer.layer_changed.connect(self.update_layers, inst=layer)


    def rmv_layer(self, layer):
        layer.layer_changed.disconnect(self.update_layers, inst=layer)

        self.removeItem(layer)
        self.update()


    def update_layers(self, layer=None):
        self.update()