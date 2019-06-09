from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class FileBrowser(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout = QVBoxLayout()

        self.file_system_model = QFileSystemModel()
        self.file_tree_view    = QTreeView()


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.file_tree_view)


    def update_gui(self):
        self.file_system_model.setNameFilters(('*.osu', '*.osr'))
        self.file_system_model.setNameFilterDisables(False)
        self.file_system_model.setRootPath(QDir.currentPath())

        self.file_tree_view.setDragEnabled(True)
        self.file_tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.file_tree_view.setModel(self.file_system_model)
        self.file_tree_view.hideColumn(1)   # Hide file size column
        self.file_tree_view.hideColumn(2)   # Hide file type column
        self.file_tree_view.setRootIndex(self.file_system_model.index(QDir.currentPath()))
        self.file_tree_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.file_tree_view.resizeColumnToContents(0)   # Resize file name column