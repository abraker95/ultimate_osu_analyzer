from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class PlayfieldManager(QTabWidget):

    def __init__(self):
        super().__init__()


    def get_current_playfield(self):
        return self.widget(self.currentIndex())


    def playfield_layer_changed(self):
        playfield = self.get_current_playfield()
        if not playfield: return

        playfield.layer_changed()


    def playfield_remove_layer(self, layer_name):
        playfield = self.get_current_playfield()
        if not playfield: return

        playfield.remove_layer(layer_name)
        

    def playfield_set_time(self, time):
        playfield = self.get_current_playfield()
        if not playfield: return

        playfield.set_time(time)