from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.osu_playfield import OsuPlayField
from osu.local.beatmap.beatmap import Beatmap


class PlayFieldTest(QMainWindow):

    title = 'Ultimate osu! analyzer widget test'
    left   = 100
    top    = 100
    width  = 1080
    height = 720

    def __init__(self, beatmap_filepath, parent=None):

        super(PlayFieldTest, self).__init__(parent)

        beatmap = Beatmap(beatmap_filepath)

        self.widget = OsuPlayField(beatmap)
        self.setCentralWidget(self.widget)

        self.setWindowTitle(PlayFieldTest.title)
        self.setGeometry(PlayFieldTest.left, PlayFieldTest.top, PlayFieldTest.width, PlayFieldTest.height)
        self.show()