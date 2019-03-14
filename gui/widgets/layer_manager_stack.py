from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.layer_manager import LayerManager
from misc.callback import callback


class LayerManagerStack(QWidget):

    def __init__(self):
        super().__init__()

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layer_stack = QStackedWidget()
        self.layout      = QVBoxLayout()

        self.layer_managers = {}


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.layer_stack)

    
    def update_gui(self):
        pass


    def add_layer_manager(self, name):
        if name in self.layer_managers: return

        layer_manager = LayerManager(name)
        self.layer_stack.addWidget(layer_manager)
        self.layer_managers[name] = self.layer_stack.indexOf(layer_manager)


    def remove_layer_manager(self, name):
        self.layer_stack.removeWidget(self.layer_managers[name])
        self.layer_managers[name].deleteLater()
        del self.layer_managers[name]


    def get_layer_manager(self, name):
        return self.layer_stack.widget(self.layer_managers[name])


    def set_layer_manager_active(self, name):
        self.layer_stack.setCurrentIndex(self.layer_managers[name])