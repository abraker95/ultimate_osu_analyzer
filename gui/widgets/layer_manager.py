from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.layer_controller import LayerController
from misc.callback import callback


class LayerManager(QWidget):

    def __init__(self, name):
        super().__init__()

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()

        self.name = name


    def init_gui_elements(self):
        self.layout            = QVBoxLayout()
        self.layer_controllers = {}


    def construct_gui(self):
        self.setLayout(self.layout)

    
    def update_gui(self):
        pass


    @callback
    def remove_layer_event(self, layer_name):
        self.remove_layer_event.emit(layer_name)


    @callback
    def layer_change_event(self):
        self.layer_change_event.emit()


    def add_layer(self, layer):
        if layer.name in self.layer_controllers: return

        self.layer_controllers[layer.name] = LayerController(layer)
        self.layout.addWidget(self.layer_controllers[layer.name])

        self.layer_controllers[layer.name].layer_change_event.connect(self.layer_change_event)
        self.layer_controllers[layer.name].layer_destroy_event.connect(self.remove_layer_event)