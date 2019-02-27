import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from unit_tests.beatmap_tests import BeatmapTests
from unit_tests.playfield_test import PlayFieldTest


sys._excepthook = sys.excepthook 
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback) 
    sys.exit(1) 

sys.excepthook = exception_hook 


if __name__ == '__main__':
    print('Running beatmap loading test mania . . .')
    BeatmapTests.test_beatmap_loading_mania('unit_tests\\Camellia - GHOST (qqqant) [Collab PHANTASM [MX]].osu')
    print('OK\n\n')

    print('Running beatmap loading test std . . .')
    BeatmapTests.test_beatmap_loading_std('unit_tests\\Mutsuhiko Izumi - Red Goose (nold_1702) [ERT Basic].osu')
    print('OK\n\n')

    # test_hitobject_visibility_std()

    app = QApplication(sys.argv)
    ex  = PlayFieldTest('unit_tests\\abraker - unknown (abraker) [250ms].osu')
    sys.exit(app.exec_())