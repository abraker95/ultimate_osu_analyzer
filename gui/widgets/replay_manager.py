from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from enum import Enum

from analysis.osu.std.replay_data import StdReplayData
#from analysis.osu.taiko.replay_data import TaikoReplayData
#from analysis.osu.catch.replay_data import CatchReplayData
from analysis.osu.mania.replay_data import ManiaReplayData

from osrparse.enums import GameMode
from cli.cmd_osu import CmdOsu


class Column(Enum):

    PLAYER_NAME = 0
    MODS        = 1
    SCORE       = 2
    COMBO       = 3
    ACCURACY    = 4
    HITS_300    = 5
    HITS_100    = 6
    HITS_50     = 7
    HITS_0      = 8
    NUM_COLS    = 9


class ReplayManagerItem(QTreeWidgetItem):

    def __init__(self, replay, columns):
        QTreeWidgetItem.__init__(self, columns)
        self.replay      = replay
        self.replay_data = None


    def __lt__(self, other):
        column = self.treeWidget().sortColumn()

        if column == Column.PLAYER_NAME.value: return QTreeWidgetItem.__lt__(self, other)                   # string sort
        if column == Column.MODS.value:        return QTreeWidgetItem.__lt__(self, other)                   # string sort
        if column == Column.SCORE.value:       return float(self.text(column)) < float(other.text(column))  # numeric sort
        if column == Column.COMBO.value:       return float(self.text(column)) < float(other.text(column))  # numeric sort
        if column == Column.ACCURACY.value:    return float(self.text(column)) < float(other.text(column))  # numeric sort
        if column == Column.HITS_300.value:    return float(self.text(column)) < float(other.text(column))  # numeric sort
        if column == Column.HITS_100.value:    return float(self.text(column)) < float(other.text(column))  # numeric sort
        if column == Column.HITS_50.value:     return float(self.text(column)) < float(other.text(column))  # numeric sort
        if column == Column.HITS_0.value:      return float(self.text(column)) < float(other.text(column))  # numeric sort


    def get_replay_data(self):
        if self.replay_data == None:
            if   self.replay.game_mode == GameMode.Standard:     self.replay_data = StdReplayData.get_event_data(self.replay.play_data)
            #elif self.replay.game_mode == GameMode.Taiko:        self.replay_data = TaikoReplayData.get_event_data(self.replay.play_data)
            #elif self.replay.game_mode == GameMode.CatchTheBeat: self.replay_data = CatchReplayData.get_event_data(self.replay.play_data)
            #elif self.replay.game_mode == GameMode.Osumania:     self.replay_data = ManiaReplayData.get_replay_data(self.replay.play_data, columns)
            else:
                RuntimeError('Unsupported gamemode: ' + str(self.replay.game_mode))

        return self.replay_data



class ReplayManager(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout      = QVBoxLayout()
        self.replay_list = QTreeWidget()


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.replay_list)


    def update_gui(self):
        self.replay_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.replay_list.customContextMenuRequested.connect(self.__right_click_menu)
        self.replay_list.setRootIsDecorated(False)
        self.replay_list.setSortingEnabled(True)

        columns = ('player', 'mods', 'score', 'combo', 'acc', '300', '100', '50', 'miss')
        self.replay_list.setHeaderLabels(columns)
        self.replay_list.header().setStretchLastSection(False)
        self.replay_list.header().setSectionResizeMode(QHeaderView.ResizeToContents)


    def add_replay(self, replay):
        columns = (replay.player_name, replay.get_mods_name(), str(replay.score), str(replay.max_combo), str(replay.get_acc()),
                   str(replay.number_300s + replay.gekis), str(replay.number_100s + replay.katus), str(replay.number_50s), str(replay.misses))
        self.replay_list.addTopLevelItem(ReplayManagerItem(replay, columns))

        for i in range(Column.NUM_COLS.value):
            self.replay_list.resizeColumnToContents(i)


    def rmv_replay(self, replay):
        print('TODO: rmv replay')


    def __right_click_menu(self, pos):
        item = self.replay_list.itemAt(pos)
        if item == None: return

        set_visible_action = QAction('&Set only this visible')
        set_visible_action.setStatusTip('Hides all other replay layers')
        set_visible_action.triggered.connect(lambda _, item=item: self.__set_this_visible(item))

        create_offset_graph_action = QAction('&Create offset graph')
        create_offset_graph_action.setStatusTip('Add an offset graph to the Graphs tab')
        create_offset_graph_action.triggered.connect(lambda _, item=item: self.__create_offset_graph(item))

        locate_replay_action = QAction('&Locate Replay')
        locate_replay_action.setStatusTip('Locates replay in file browser')
        locate_replay_action.triggered.connect(lambda _, item=item: self.__locate_replay(item))

        copy_replay_code_action = QAction('&Copy replay code to clipboard')
        copy_replay_code_action.setStatusTip('Copies the code needed to access the replay to clipboard')
        copy_replay_code_action.triggered.connect(lambda _, item=item: self.__replay_code_to_clipboard(item))

        # TODO: Figure out how to get available replay layers
        # layer_menu = QMenu()

        menu = QMenu(self)
        menu.addAction(set_visible_action)
        menu.addAction(create_offset_graph_action)
        menu.addAction(locate_replay_action)
        menu.addAction(copy_replay_code_action)
        menu.exec(self.replay_list.mapToGlobal(pos))


    def __set_this_visible(self, item):
        print('TODO: __set_this_visible')


    def __create_offset_graph(self, item):
        replay_data = item.get_replay_data()
        CmdOsu.create_offset_graph(replay_data)


    def __locate_replay(self, item):
        print('TODO: __locate_replay')


    def __replay_code_to_clipboard(self, item):
        print('TODO: __replay_code_to_clipboard')