from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class PlayfieldManager(QTabWidget):

    def __init__(self):
        super().__init__()


    def get_current_playfield(self):
        return self.widget(self.currentIndex())


    def playfield_layer_changed(self):
        self.get_current_playfield().layer_changed()


    def playfield_remove_layer(self, layer_name):
        self.get_current_playfield().remove_layer(layer_name)
        

    def playfield_set_time(self, time):
        self.get_current_playfield().set_time(time)