from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph

from misc.callback import callback


class LinePlot(pyqtgraph.PlotCurveItem):

    def __init__(self):
        super().__init__()


    def update_data(self, data):
        data_x, data_y = data
        self.setData(x=data_x, y=data_y)