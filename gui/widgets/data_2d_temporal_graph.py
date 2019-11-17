from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph


from misc.callback import callback
from gui.objects.graph.scatter_plot import ScatterPlot
from gui.objects.graph.line_plot import LinePlot


class Data2DTemporalGraph(pyqtgraph.PlotWidget):

    SCATTER_PLOT = 0
    LINE_PLOT    = 1

    MIN_TIME     = -5000

    @callback
    def __init__(self, name, data_2d, plot_type=None):
        super().__init__()

        pyqtgraph.setConfigOptions(antialias=True)

        #self.showAxis('left', show=False)
        self.setLimits(xMin=Data2DTemporalGraph.MIN_TIME)
        self.setRange(xRange=(-100, 10000))

        self.getViewBox().setMouseEnabled(y=False)
        self.getPlotItem().setTitle(name)

        if   plot_type == Data2DTemporalGraph.SCATTER_PLOT: self.plot_item = ScatterPlot()
        elif plot_type == Data2DTemporalGraph.LINE_PLOT:    self.plot_item = LinePlot()
        else:                                               self.plot_item = ScatterPlot()
        self.addItem(self.plot_item)

        self.timeline_marker = pyqtgraph.InfiniteLine(angle=90, movable=True)
        self.timeline_marker.setBounds((Data2DTemporalGraph.MIN_TIME + 100, None))
        self.timeline_marker.sigPositionChanged.connect(self.time_changed_event)
        self.addItem(self.timeline_marker, ignoreBounds=True)
        
        self.update_data(data_2d)
        self.__init__.emit(self)


    @callback
    def __del__(self):
        self.__del__.emit(self)


    def update_data(self, data_2d):
        # Filter out infinities
        data_x, data_y = data_2d
        inf_idx_filter = np.where(np.isfinite(np.asarray(data_y).astype(np.float64)))
        data_x, data_y = data_x[inf_idx_filter], data_y[inf_idx_filter]
        
        self.plot_item.update_data((data_x, data_y))
        if len(data_x) > 0: self.setRange(xRange=(data_x[0] - 100, data_x[-1] + 100))
        if len(data_y) > 0: self.setRange(yRange=(min(data_y), max(data_y)))

        self.setLimits(xMin=data_x[0] - 1000, xMax=data_x[-1] + 1000)


    def update_graph_info(self, title=None, x_axis_label=None, y_axis_label=None):
        if title:        self.getPlotItem().setTitle(title=title)
        if x_axis_label: self.getPlotItem().setLabel('bottom', text=x_axis_label)
        if y_axis_label: self.getPlotItem().setLabel('left',   text=y_axis_label)

    
    def get_name(self):
        return self.getPlotItem().titleLabel.text

    
    @callback
    def time_changed_event(self, marker):
        self.time_changed_event.emit(marker.value())