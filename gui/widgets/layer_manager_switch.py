from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.layer_gui import LayerGui
from gui.widgets.QContainer import QContainer

from generic.switcher import Switcher



class LayerManagerSwitch(QWidget, Switcher):

    def __init__(self):
        QWidget.__init__(self)
        Switcher.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layer_stack = QStackedWidget()
        self.layout      = QVBoxLayout()


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.layer_stack)

        self.switch.connect(self.switch_layer_manager, inst=self)

    
    def update_gui(self):
        pass


    def add_layer(self, layer):
        self.layer_stack.currentWidget().addWidget(LayerGui(layer))


    def add_layer_manager(self, layer_manager):
        layer_manager_gui = QContainer(QVBoxLayout())
        for layer in layer_manager.data.values():
            layer_manager_gui.get().addWidget(LayerGui(layer))

        layer_manager.add_layer.connect(self.add_layer, inst=layer_manager)

        new_idx = self.layer_stack.addWidget(layer_manager_gui) 
        self.layer_stack.setCurrentIndex(new_idx)


    def rmv_layer_manager(self, layer_manager):
        old_mgr = self.layer_stack.currentWidget()        
        self.layer_stack.removeWidget(old_mgr)
        
        layer_manager.add_layer.disconnect(self.add_layer, inst=old_mgr)
        if old_mgr:
            old_mgr.deleteLater()
            old_mgr = None


    def switch_layer_manager(self, old_layer_manager, new_layer_manager):
        if old_layer_manager: self.rmv_layer_manager(old_layer_manager)
        if new_layer_manager: self.add_layer_manager(new_layer_manager)