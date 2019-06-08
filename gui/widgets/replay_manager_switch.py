from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.QContainer import QContainer

from generic.switcher import Switcher



class ReplayManagerSwitch(QWidget, Switcher):

    def __init__(self):
        QWidget.__init__(self)
        Switcher.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.replay_stack = QStackedWidget()
        self.layout       = QVBoxLayout()


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.replay_stack)

        self.switch.connect(self.__switch_replay_manager, inst=self)

    
    def update_gui(self):
        pass


    def add_replay(self, replay):
        self.replay_stack.currentWidget().add_replay(replay)


    def rmv_replay(self, replay):
        self.replay_stack.currentWidget().rmv_replay(replay)


    def __add_replay_manager(self, replay_manager_gui):
        new_idx = self.replay_stack.addWidget(replay_manager_gui) 
        self.replay_stack.setCurrentIndex(new_idx)


    def __rmv_replay_manager(self, replay_manager):
        old_mgr = self.replay_stack.currentWidget()        
        self.replay_stack.removeWidget(old_mgr)


    def __switch_replay_manager(self, old_replay_manager, new_replay_manager):
        if old_replay_manager != None: self.__rmv_replay_manager(old_replay_manager)
        if new_replay_manager != None: self.__add_replay_manager(new_replay_manager)