from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from enum import Enum

from analysis.osu.std.replay_data import StdReplayData
#from analysis.osu.taiko.replay_data import TaikoReplayData
#from analysis.osu.catch.replay_data import CatchReplayData
from analysis.osu.mania import ManiaReplayData

from osrparse.enums import GameMode
from cli.cmd_osu import CmdOsu


class Column(Enum):

    NUM         = 0
    PLAYER_NAME = 1
    MODS        = 2
    SCORE       = 3
    COMBO       = 4
    ACCURACY    = 5
    HITS_300    = 6
    HITS_100    = 7
    HITS_50     = 8
    HITS_0      = 9
    NUM_COLS    = 10


class ReplayManagerItem(QTreeWidgetItem):

    def __init__(self, replay, num):
        self.replay      = replay
        self.replay_data = None
        
        if self.replay.game_mode == GameMode.Standard: 
            columns = (str(num), replay.player_name, replay.get_mods_name(), str(replay.score), str(replay.max_combo), str(replay.get_acc()),
                        str(replay.number_300s + replay.gekis), str(replay.number_100s + replay.katus), str(replay.number_50s), str(replay.misses))
        #elif self.replay.game_mode == GameMode.Taiko:        
        #    columns = ()
        #elif self.replay.game_mode == GameMode.CatchTheBeat:
        #    columns = ()
        elif self.replay.game_mode == GameMode.Osumania:    
             columns = (str(num), replay.player_name, replay.get_mods_name(), str(replay.score), str(replay.max_combo), str(replay.get_acc()),
                        str(replay.gekis), str(replay.number_300s), str(replay.katus), str(replay.number_100s), str(replay.number_50s), str(replay.misses))
        else:
            RuntimeError('Unsupported gamemode: ' + str(self.replay.game_mode))

        QTreeWidgetItem.__init__(self, columns)


    def __lt__(self, other):
        column = self.treeWidget().sortColumn()

        if column == Column.NUM.value:         return int(self.text(column)) < int(other.text(column))      # numeric sort
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
        if type(self.replay_data) == type(None):
            if   self.replay.game_mode == GameMode.Standard:     self.replay_data = StdReplayData.get_replay_data(self.replay.play_data)
            #elif self.replay.game_mode == GameMode.Taiko:        self.replay_data = TaikoReplayData.get_replay_data(self.replay.play_data)
            #elif self.replay.game_mode == GameMode.CatchTheBeat: self.replay_data = CatchReplayData.get_replay_data(self.replay.play_data)
            elif self.replay.game_mode == GameMode.Osumania:     self.replay_data = ManiaReplayData.get_replay_data(self.replay.play_data, self.replay.mania_keys)
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
        self.replay_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.replay_list.setRootIsDecorated(False)
        self.replay_list.setSortingEnabled(True)

        self.replay_list.header().setStretchLastSection(False)
        self.replay_list.header().setSectionResizeMode(QHeaderView.ResizeToContents)


    def add_replay(self, replay):
        if self.replay_list.topLevelItemCount() == 0:
            if   replay.game_mode == GameMode.Standard: columns = ('#', 'player', 'mods', 'score', 'combo', 'acc', '300', '100', '50', 'miss')
            #elif self.replay.game_mode == GameMode.Taiko:        self.replay_data = TaikoReplayData.get_replay_data(self.replay.play_data)
            #elif self.replay.game_mode == GameMode.CatchTheBeat: self.replay_data = CatchReplayData.get_replay_data(self.replay.play_data)
            elif replay.game_mode == GameMode.Osumania: columns = ('#', 'player', 'mods', 'score', 'combo', 'acc', 'MAX', '300', '200', '100', '50', 'miss')
            else:
                RuntimeError('Unsupported gamemode: ' + str(replay.game_mode))
            
            self.replay_list.setHeaderLabels(columns)

        self.replay_list.addTopLevelItem(ReplayManagerItem(replay, self.replay_list.topLevelItemCount()))

        for i in range(Column.NUM_COLS.value):
            self.replay_list.resizeColumnToContents(i)


    def rmv_replay(self, replay):
        print('TODO: rmv replay')


    def get_replay_data(self, start=None, end=None):
        start = max(0, start) if start != None else 0
        end   = min(self.replay_list.topLevelItemCount(), end) if end != None else self.replay_list.topLevelItemCount()

        return [ self.replay_list.topLevelItem(i).get_replay_data() for i in range(start, end) ]

    
    def get_replays(self, start=None, end=None):
        start = max(0, start) if start != None else 0
        end   = min(self.replay_list.topLevelItemCount(), end) if end != None else self.replay_list.topLevelItemCount()

        return [ self.replay_list.topLevelItem(i).replay for i in range(start, end) ]


    def __right_click_menu(self, pos):
        selected = self.replay_list.selectedItems()
        if len(selected) == 0: return

        if len(selected) == 1:
            item = selected[0]

            # Main menu items
            set_visible_action = QAction('&Set only this visible')
            set_visible_action.setStatusTip('Hides all other replay layers')
            set_visible_action.triggered.connect(lambda _, item=item: self.__set_this_visible(item))

            # TODO: Figure out how to get available replay layers
            # layer_menu = QMenu()

            locate_replay_action = QAction('&Locate Replay')
            locate_replay_action.setStatusTip('Locates replay in file browser')
            locate_replay_action.triggered.connect(lambda _, item=item: self.__locate_replay(item))

            copy_replay_code_action = QAction('&Copy replay code to clipboard')
            copy_replay_code_action.setStatusTip('Copies the code needed to access the replay to clipboard')
            copy_replay_code_action.triggered.connect(lambda _, item=item: self.__replay_code_to_clipboard(item))

            copy_score_code_action = QAction('&Copy score code to clipboard')
            copy_score_code_action.setStatusTip('Copies the code needed to access the score to clipboard')
            copy_score_code_action.triggered.connect(lambda _, item=item: self.__score_code_to_clipboard(item))

            # Menu construction
            menu = QMenu(self)
            #menu.addAction(set_visible_action)     # TODO
            #menu.addAction(locate_replay_action)   # TODO
            menu.addAction(copy_replay_code_action)
            menu.addAction(copy_score_code_action)

            menu.exec(self.replay_list.mapToGlobal(pos))
        else:
            probabilistic_analysis_action = QAction('&Probabilistic analysis')
            probabilistic_analysis_action.setStatusTip('Calculate odds of players hitting hitobject')
            probabilistic_analysis_action.triggered.connect(lambda _, item=selected: self.__probabilistic_analysis(selected))

            copy_per_hitobject_score_code_action = QAction('&Copy per-hitobject score code to clipboard')
            copy_per_hitobject_score_code_action.setStatusTip('Copies the code needed to access the per-hitobject scores to clipboard')
            copy_per_hitobject_score_code_action.triggered.connect(lambda _, item=selected: self.__per_hitobject_score_code_to_clipboard(selected))

            menu = QMenu(self)
            #menu.addAction(probabilistic_analysis_action)
            menu.addAction(copy_per_hitobject_score_code_action)

            # TODO: Mass toggle visibility
            # TODO: Replay code range
            # TODO: Average of replays for graphs
            # TODO: probabilistic analysis

            menu.exec(self.replay_list.mapToGlobal(pos))


    def __set_this_visible(self, item):
        print('TODO: __set_this_visible')


    def __locate_replay(self, item):
        print('TODO: __locate_replay')


    def __replay_code_to_clipboard(self, item):
        QApplication.clipboard().setText(f'replay_data = StdReplayData.get_replay_data(get_replays()[{self.replay_list.currentIndex().row()}])')

    def __score_code_to_clipboard(self, item):
        gamemode = item.replay.game_mode

        if gamemode == GameMode.Standard:
            map_data   = 'StdMapData.get_map_data'
            score_data = 'StdScoreData'
        elif gamemode == GameMode.Taiko:
            map_data   = 'TaikoMapData.get_map_data'
            score_data = 'TaikoScoreData'
        elif gamemode == GameMode.CatchTheBeat:
            map_data   = 'CatchMapData.get_map_data'
            score_data = 'CatchscoreData'
        elif gamemode == GameMode.Osumania:
            map_data   = 'ManiaMapData.get_map_data'
            score_data = 'ManiaScoreData'
        else:
            RuntimeError('Unsupported gamemode')

        replay_data_code = f'get_replays()[{self.replay_list.currentIndex().row()}]'
        map_data_code    = map_data + '(get_beatmap().hitobjects)'
        score_data_code  = f'score_data = {score_data}.get_score_data({replay_data_code}, {map_data_code})'
        
        QApplication.clipboard().setText(score_data_code)


    def __per_hitobject_score_code_to_clipboard(self, items):
        gamemode = items[0].replay.game_mode

        if gamemode == GameMode.Standard:
            map_data           = 'StdMapData.get_map_data(get_beatmap().hitobjects)'
            score_data         = f'[ StdScoreData.get_score_data(get_replays()[i], {map_data}) for i in range({len(items)}) ]'
            per_hitobject_data = f'StdScoreMetrics.get_per_hitobject_score_data({score_data})'
        elif gamemode == GameMode.Taiko:
            map_data           = 'TaikoMapData.get_map_data(get_beatmap().hitobjects)'
            score_data         = f'[ TaikoScoreData.get_score_data(get_replays()[i], {map_data}) for i in range({len(items)}) ]'
            per_hitobject_data = f'TaikoScoreMetrics.get_per_hitobject_score_data({score_data})'
        elif gamemode == GameMode.CatchTheBeat:
            map_data           = 'CatchMapData.get_map_data(get_beatmap().hitobjects)'
            score_data         = f'[ CatchscoreData.get_score_data(get_replays()[i], {map_data}) for i in range({len(items)}) ]'
            per_hitobject_data = f'CatchScoreMetrics.get_per_hitobject_score_data({score_data})'
        elif gamemode == GameMode.Osumania:
            map_data           = 'ManiaMapData.get_map_data(get_beatmap().hitobjects)'
            score_data         = f'[ ManiaScoreData.get_score_data(get_replays()[i], {map_data}) for i in range({len(items)}) ]'
            per_hitobject_data = f'ManiaScoreMetrics.get_per_hitobject_score_data({score_data})'
        else:
            RuntimeError('Unsupported gamemode')

        per_hitobject_data = 'per_hitobject_data = ' + per_hitobject_data
        
        QApplication.clipboard().setText(per_hitobject_data)