from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph
import numpy as np



class ScatterPlot(pyqtgraph.ScatterPlotItem):

    def __init__(self):
        super().__init__()

        self.setSize(10)
        self.setPen(pyqtgraph.mkPen(None))
        self.setBrush(pyqtgraph.mkBrush(255, 255, 255, 120))


    def update_data(self, data_x, data_y):
        if type(data_x) == type(None) or type(data_y) == type(None):
            self.clear()
            return

        # Filter out infinities
        inf_filter = np.isfinite(data_y.astype(np.float64))
        data_x, data_y = data_x[inf_filter], data_y[inf_filter]

        self.clear()
        self.addPoints(x=data_x, y=data_y)

        return data_x, data_y