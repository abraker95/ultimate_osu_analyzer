from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#from gui.widgets. import graphGui
from gui.widgets.QContainer import QContainer

from generic.switcher import Switcher



class GraphManagerSwitch(QWidget, Switcher):

    def __init__(self):
        QWidget.__init__(self)
        Switcher.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.graph_stack = QStackedWidget()
        self.layout      = QVBoxLayout()


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.graph_stack)

        self.switch.connect(self.__switch_graph_manager, inst=self)

    
    def update_gui(self):
        pass


    def add_graph(self, graph):
        self.graph_stack.currentWidget().addWidget(graph)


    def __add_graph_manager(self, graph_manager_gui):
        new_idx = self.graph_stack.addWidget(graph_manager_gui) 
        self.graph_stack.setCurrentIndex(new_idx)


    def __rmv_graph_manager(self, graph_manager):
        old_mgr = self.graph_stack.currentWidget()        
        self.graph_stack.removeWidget(old_mgr)


    def __switch_graph_manager(self, old_graph_manager, new_graph_manager):
        if old_graph_manager != None: self.__rmv_graph_manager(old_graph_manager)
        if new_graph_manager != None: self.__add_graph_manager(new_graph_manager)