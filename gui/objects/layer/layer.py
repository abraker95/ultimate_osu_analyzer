from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback


class Layer(QGraphicsItem):


    def __init__(self, name):
        QGraphicsItem.__init__(self)

        self.name = name


    def area_resize_event(self, width, height):
        raise NotImplementedError()

        # Reminder this needs to be put in the 
        # implementation of derived class
        self.layer_changed()


    @callback
    def layer_changed(self):
        self.layer_changed.emit(inst=self)

    
    def boundingRect(self):
        return QRectF(0, 0, 0, 0)