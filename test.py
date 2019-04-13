import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from unit_tests.callback_test import CallbackTest
from unit_tests.beatmap_tests import BeatmapTests
from unit_tests.playfield_test import PlayFieldTest
from unit_tests.temporal_graph_test import TemporalGraphTest
from unit_tests.graph_manager_test import GraphManagerTest
from unit_tests.layer_controller_test import LayerControllerTest


sys._excepthook = sys.excepthook 
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback) 
    sys.exit(1) 

sys.excepthook = exception_hook 


if __name__ == '__main__':

    CallbackTest.run_tests()
    
    print('Running beatmap loading test mania . . .')
    BeatmapTests.test_beatmap_loading_mania('unit_tests\\maps\\Camellia - GHOST (qqqant) [Collab PHANTASM [MX]].osu')
    print('OK\n\n')

    print('Running beatmap loading test std . . .')
    BeatmapTests.test_beatmap_loading_std('unit_tests\\maps\\Mutsuhiko Izumi - Red Goose (nold_1702) [ERT Basic].osu')
    print('OK\n\n')

    print('Running std hitobjet visibility test . . .')
    # BeatmapTests.test_hitobject_visibility_std()
    print('OK\n\n')

    app = QApplication(sys.argv)

    play_field_test = PlayFieldTest('unit_tests\\maps\\abraker - unknown (abraker) [250ms].osu')
    play_field_test.time_browse_test(app)
    play_field_test.layer_toggle_test()
    play_field_test.close()

    temporal_graph_test = TemporalGraphTest()
    temporal_graph_test.time_minupilation_test(app)
    temporal_graph_test.close()

    graph_manager_test = GraphManagerTest()
    graph_manager_test.run_tests(app)
    graph_manager_test.close()

    layer_controller_test = LayerControllerTest()
    layer_controller_test.visibility_toggle_test(app)
    time.sleep(1)
    layer_controller_test.close()
    