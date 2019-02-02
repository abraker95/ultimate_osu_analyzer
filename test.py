import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from unit_tests.beatmap_tests import BeatmapTests
from unit_tests.playfield_test import PlayFieldTest



if __name__ == '__main__':
    print('Running beatmap loading test mania . . .')
    BeatmapTests.test_beatmap_loading_mania('unit_tests\\Camellia - GHOST (qqqant) [Collab PHANTASM [MX]].osu')
    print('OK\n\n')

    print('Running beatmap loading test std . . .')
    BeatmapTests.test_beatmap_loading_std('unit_tests\\Mutsuhiko Izumi - Red Goose (nold_1702) [ERT Basic].osu')
    print('OK\n\n')

    app = QApplication(sys.argv)
    ex  = PlayFieldTest('unit_tests\\Mutsuhiko Izumi - Red Goose (nold_1702) [ERT Basic].osu')
    sys.exit(app.exec_())