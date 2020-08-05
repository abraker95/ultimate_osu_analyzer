from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph

import numpy as np



class BarPlot(pyqtgraph.BarGraphItem):

    def __init__(self):
        super().__init__()


    def update_data(self, num_bins, data_y, color='b'):
        if type(num_bins) == type(None) or type(data_y) == type(None):
            self.setOpts(**{
                'x'      : [],
                'height' : [],
                'width'  : 0.5
            })
            return

        # Filter out infinities
        data_y = data_y[np.isfinite(data_y.astype(np.float64))]

        # Calculate histogram data
        data_y, data_x = np.histogram(data_y, num_bins)
        data_x = (data_x[1:] + data_x[:-1])/2
        width = (data_x[-1] - data_x[0])/len(data_x)

        self.setOpts(**{
            'x'      : data_x,
            'height' : data_y,
            'width'  : width
        })

        return data_x, data_y