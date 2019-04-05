from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph

from misc.callback import callback


class ScatterPlot(pyqtgraph.ScatterPlotItem):

    def __init__(self):
        super().__init__()

        self.setSize(10)
        self.setPen(pyqtgraph.mkPen(None))
        self.setBrush(pyqtgraph.mkBrush(255, 255, 255, 120))


    def update_data(self, data):
        data_x, data_y = data
        self.addPoints(x=data_x, y=data_y)