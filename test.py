import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from unit_tests.callback_test import CallbackTest
from unit_tests.beatmap_tests import BeatmapTests
from unit_tests.temporal_graph_test import TemporalGraphTest
from unit_tests.graph_manager_test import GraphManagerTest
from unit_tests.manager_switch_test import ManagerSwitchTest
from unit_tests.std_replay_test import StdReplayTest
from unit_tests.display_test import DisplayTest


sys._excepthook = sys.excepthook 
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback) 
    sys.exit(1) 

sys.excepthook = exception_hook 


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    CallbackTest.run_tests()

    print('Running beatmap loading test mania . . .')
    BeatmapTests.test_beatmap_loading_mania('unit_tests\\maps\\Camellia - GHOST (qqqant) [Collab PHANTASM [MX]].osu')
    print('OK\n\n')

    print('Running beatmap loading test std . . .')
    BeatmapTests.test_beatmap_loading_std('unit_tests\\maps\\Mutsuhiko Izumi - Red Goose (nold_1702) [ERT Basic].osu')
    print('OK\n\n')

    print('Running std hitobject visibility test . . .')
    # BeatmapTests.test_hitobject_visibility_std()
    print('OK\n\n')

    display_test = DisplayTest(app, 'unit_tests\\maps\\Mutsuhiko Izumi - Red Goose (nold_1702) [ERT Basic].osu')
    display_test.switcher_test()
    display_test.time_browse_test(app)
    display_test.close()

    std_replay_test = StdReplayTest(app)
    std_replay_test.close()

    manager_switch_test = ManagerSwitchTest()
    manager_switch_test.manager_switch_test()
    manager_switch_test.manager_add_remove_test()

    temporal_graph_test = TemporalGraphTest()
    temporal_graph_test.time_minupilation_test(app)
    temporal_graph_test.close()

    graph_manager_test = GraphManagerTest()
    graph_manager_test.run_tests(app)
    graph_manager_test.close()