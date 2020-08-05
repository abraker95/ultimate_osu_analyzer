from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph
import numpy as np



class LinePlot(pyqtgraph.PlotCurveItem):

    def __init__(self):
        super().__init__()


    def update_data(self, data_x, data_y):
        if type(data_x) == type(None) or type(data_y) == type(None):
            self.setData(x=[], y=[])
            return

        # Filter out infinities
        inf_filter = np.isfinite(data_y.astype(np.float64))
        data_x, data_y = data_x[inf_filter], data_y[inf_filter]

        self.setData(x=data_x, y=data_y)
        return data_x, data_y

    
    def update_xy(self, data_x, data_y):
        self.setData(x=data_x, y=data_y)