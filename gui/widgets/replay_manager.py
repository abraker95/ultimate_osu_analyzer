from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class ReplayManager(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout      = QVBoxLayout()
        self.replay_list = QListWidget()
        #self.label  = QLabel('Replay Manager')


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.replay_list)
        #self.layout.addWidget(self.label)


    def update_gui(self):
        #self.label.setAlignment(Qt.AlignCenter)
        pass


    def add_replay(self, replay):
        self.replay_list.addItem(replay.get_name())
        print('TODO: Make it QListWidgetItem')


    def rmv_replay(self, replay):
        print('TODO: rmv replay')