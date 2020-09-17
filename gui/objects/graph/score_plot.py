from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph
import numpy as np

from analysis.osu.std.score_data import StdScoreData


class ScorePlot(pyqtgraph.ScatterPlotItem):

    def __init__(self, time, score_type, yoffset=0):
        super().__init__()

        self.setSize(10)
        self.setPen(pyqtgraph.mkPen(None))

        self.update_data(time, score_type, yoffset)


    def update_data(self, time, score_type, yoffset=0):
        if type(time) == type(None) or type(time) == type(None):
            self.clear()
            return

        color_map = {
            StdScoreData.TYPE_MISS : (255,  100, 100, 255),  # Red
            StdScoreData.TYPE_HITP : (100,  255, 100, 255),  # Green
            StdScoreData.TYPE_HITR : ( 50,  150, 255, 255),  # Blue
            StdScoreData.TYPE_AIMH : ( 150, 100, 255, 255),  # Purple
        }

        y = [ yoffset for _ in range(len(time)) ]
        b = [ pyqtgraph.mkBrush(*color_map[a]) for a in score_type.values ]

        self.clear()
        self.addPoints(x=time, y=y, brush=b)

        return time, y