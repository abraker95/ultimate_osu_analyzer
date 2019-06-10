from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.objects.group import Group
from gui.objects.scene import Scene

from misc.callback import callback



class LayerManagerItem(QTreeWidgetItem):

    def __init__(self, data):
        self.layer = data
        columns = (self.layer.name, )

        QTreeWidgetItem.__init__(self, columns)
        
        self.setCheckState(0, Qt.Checked)  # Set checked on 0th column


    def layer_enable_event(self):
        # Set visibility to whatever the check state is
        self.layer.setVisible(self.checkState(0)) 
        self.layer.layer_changed()



class LayerManager(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()

        self.scene = Scene()


    def init_gui_elements(self):
        self.layout     = QVBoxLayout()
        self.layer_list = QTreeWidget()


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.layer_list)


    def update_gui(self):
        self.layer_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.layer_list.customContextMenuRequested.connect(self.__right_click_menu)

        self.layer_list.header().setStretchLastSection(False)
        self.layer_list.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.layer_list.header().hide()

        self.layer_list.itemClicked.connect(self.__check_item_status)


    def add_layer(self, layer):
        self.layer_list.addTopLevelItem(LayerManagerItem(layer))
        self.scene.add_layer(layer)


    def rmv_layer(self, layer):
        self.scene.rmv_layer(layer)


    def get_scene(self):
        return self.scene


    def __check_item_status(self, item):
        item.layer_enable_event()


    def __right_click_menu(self, pos):
        item = self.layer_list.itemAt(pos)
        if item == None: return

        # TODO