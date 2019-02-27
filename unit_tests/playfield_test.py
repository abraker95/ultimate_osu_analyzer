from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.playfield import Playfield
from osu.local.beatmap.beatmap import Beatmap


class PlayFieldTest(QMainWindow):

    title = 'Ultimate osu! analyzer widget test'
    left   = 100
    top    = 100
    width  = 1080
    height = 720

    def __init__(self, beatmap_filepath):
        QMainWindow.__init__(self)
        
        self.playfield = Playfield()
        self.playfield.setFocusPolicy(Qt.NoFocus)

        self.beatmap = Beatmap(beatmap_filepath)
        self.playfield.load_beatmap(self.beatmap)

        self.setCentralWidget(self.playfield)

        self.setWindowTitle(PlayFieldTest.title)
        self.setGeometry(0, 0, self.playfield.width(), self.playfield.height())
        self.show()


    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            self.playfield.set_time(self.playfield.time - 50)

        if key == Qt.Key_Right:
            self.playfield.set_time(self.playfield.time + 50)