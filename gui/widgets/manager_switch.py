from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.QContainer import QContainer

from generic.switcher import Switcher



class ManagerSwitch(QWidget, Switcher):

    def __init__(self):
        QWidget.__init__(self)
        Switcher.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.stack  = QStackedWidget()
        self.layout = QVBoxLayout()


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.stack)

        self.switch.connect(self.__switch_manager, inst=self)

    
    def update_gui(self):
        pass


    def __add_manager(self, manager_gui):
        new_idx = self.stack.addWidget(manager_gui) 
        self.stack.setCurrentIndex(new_idx)


    def __rmv_manager(self, manager_gui):
        old_mgr = self.stack.currentWidget()        
        self.stack.removeWidget(old_mgr)


    def __switch_manager(self, old_manager, new_manager):
        if old_manager != None: self.__rmv_manager(old_manager)
        if new_manager != None: self.__add_manager(new_manager)