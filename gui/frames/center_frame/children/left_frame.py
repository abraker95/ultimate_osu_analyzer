from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.file_browser import FileBrowser
from gui.widgets.collections_browser import CollectionsBrowser
from gui.widgets.online_browser import OnlineBrowser


class LeftFrame(QFrame):
 
    def __init__(self):
        super().__init__()
        
        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout    = QHBoxLayout()
        self.tabs_area = QTabWidget()

        self.file_browser        = FileBrowser()
        self.collections_browser = CollectionsBrowser()
        self.online_browser      = OnlineBrowser()


    def construct_gui(self):
        self.setLayout(self.layout)

        self.tabs_area.addTab(self.file_browser, 'Files')
        self.tabs_area.addTab(self.collections_browser, 'Collections')
        self.tabs_area.addTab(self.online_browser, 'Online')
        self.layout.addWidget(self.tabs_area)


    def update_gui(self):
        self.setFrameShape(QFrame.StyledPanel)