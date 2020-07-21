from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph

import numpy as np

from misc.callback import callback


class BarPlot(pyqtgraph.BarGraphItem):

    def __init__(self):
        super().__init__()


    def update_data(self, data, width=0.75):
        data_x, data_y = data
        
        self.setOpts(**{
            'x'      : data_x,
            'height' : data_y,
            'width'  : width
        })