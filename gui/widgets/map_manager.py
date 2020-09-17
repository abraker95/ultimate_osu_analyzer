from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback


class MapManager(QTabBar):

    def __init__(self):
        super().__init__()

        # Allows lookup of the tab index the map is associated with
        self.data = {}

        # Add a placeholder tab and disable tab closing
        self.setTabsClosable(False)
        self.addTab('')

        self.tabMoved.connect(self.tab_moved_handler)
        self.tabCloseRequested.connect(self.map_close_event)
        self.currentChanged.connect(self.map_changed_event)
        

    def get_current_map(self):
        return self.tabData(self.currentIndex())


    def get_current_map_data(self):
        # TODO: For there to be a central place gui elements get map data from
        # because currently it needs to be recalculated every time
        pass


    def add_map(self, beatmap, name):
        # Because adding tab switches tabs before tab data is filled in
        self.currentChanged.disconnect(self.map_changed_event)
        
        # Removes the initial placeholder tab
        if self.tabText(0) == '':
            self.removeTab(0)
            self.setTabsClosable(True)

        idx = self.addTab(name)
        self.currentChanged.connect(self.map_changed_event)

        # Associate tab index with the tab the beatmap info is stored
        self.data[beatmap] = idx
        self.setTabData(idx, beatmap)
        
        # Ensure map change events are fired
        if self.currentIndex() == idx: self.map_changed_event(idx)
        else:                          self.setCurrentIndex(idx)


    def rmv_map(self, idx):
        self.removeTab(idx)


    def index_of(self, beatmap):
        return self.data[beatmap]


    def tab_insert_handler(self, idx):
        print('insert', idx)


    # Makes sure the beatmap data is associated with the tab index it's located in
    def tab_moved_handler(self, idx_from, idx_to):
        beatmap_1 = self.tabData(idx_from)
        beatmap_2 = self.tabData(idx_to)

        self.data[beatmap_1] = idx_from
        self.data[beatmap_2] = idx_to


    @callback
    def map_close_event(self, idx):
        self.map_close_event.emit(self.tabData(idx))
        del self.data[self.tabData(idx)]
        self.rmv_map(idx)

        if len(self.data) < 1:
            # Add a placeholder tab and disable tab closing
            self.setTabsClosable(False)
            self.addTab('')


    @callback
    def map_changed_event(self, idx):
        self.map_changed_event.emit(self.tabData(idx))