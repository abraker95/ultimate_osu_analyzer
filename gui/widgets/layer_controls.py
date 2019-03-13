from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.layer_controller import LayerController
from misc.callback import callback


class LayerControls(QWidget):

    def __init__(self):
        super().__init__()

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout      = QVBoxLayout()
        self.layer_ctrls = {}


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
        self.layer_ctrls[layer.name] = LayerController(layer)
        self.layout.addWidget(self.layer_ctrls[layer.name])

        self.layer_ctrls[layer.name].layer_change_event.connect(self.layer_change_event)
        self.layer_ctrls[layer.name].layer_destroy_event.connect(self.remove_layer_event)


    def clear_layer_controls(self):
        print('clear_layer_controls')
        for layer_ctrl in self.layer_ctrls.values():
            self.layout.removeWidget(layer_ctrl)
        self.layer_ctrls = {}


    # TODO: FIX This; it's bugged as hell
    def create_layer_ctrls_from_layers(self, layers):
        self.clear_layer_controls()

        # Add in new controls
        for layer in layers:
            self.add_layer(layer)