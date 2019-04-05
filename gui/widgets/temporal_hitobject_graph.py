from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph

from misc.callback import callback


class TemporalHitobjectGraph(pyqtgraph.PlotWidget):

    MIN_TIME = -5000

    def __init__(self, plot_item, name, data_func):
        super().__init__()
        pyqtgraph.setConfigOptions(antialias=True)

        self.showAxis('left', show=False)
        self.setLimits(xMin=TemporalHitobjectGraph.MIN_TIME)
        self.setRange(xRange=(-100, 10000))

        self.getViewBox().setMouseEnabled(y=False)
        self.getPlotItem().setTitle(name)

        self.plot_item = plot_item
        self.addItem(self.plot_item)

        self.timeline_marker = pyqtgraph.InfiniteLine(angle=90, movable=True)
        self.timeline_marker.setBounds((TemporalHitobjectGraph.MIN_TIME + 100, None))
        self.timeline_marker.sigPositionChanged.connect(self.time_changed_event)
        self.addItem(self.timeline_marker, ignoreBounds=True)

        self.data_func = data_func


    def update_data(self):
        data = self.data_func()
        data_x, data_y = self.validate_data(data)
        self.plot_item.update_data(data)
        
        if len(data_x) > 0: self.setRange(xRange=(data_x[0] - 100, data_x[-1] + 100))
        if len(data_y) > 0: self.setRange(yRange=(min(data_y), max(data_y)))


    def update_graph_info(self, title=None, x_axis_label=None, y_axis_label=None):
        if title:        self.getPlotItem().setTitle(title=title)
        if x_axis_label: self.getPlotItem().setLabel('bottom', text=x_axis_label)
        if y_axis_label: self.getPlotItem().setLabel('left',   text=y_axis_label)


    def update_graph_style(self, color=None, points=None):
        # TODO
        pass


    def validate_data(self, data):
        if not data: return ([], [])
        else:        return data


    def mouseDragEvent(self, event):
        event.ignore()


    @callback
    def time_changed_event(self, marker):
        self.time_changed_event.emit(marker.value())
        