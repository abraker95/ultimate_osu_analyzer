from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph

from gui.objects.graph.hitobject_plot import HitobjectPlot
from gui.objects.graph.line_plot import LinePlot
from misc.callback import callback


class Timeline(pyqtgraph.PlotWidget):

    MIN_TIME = -5000

    def __init__(self):
        super().__init__()
        pyqtgraph.setConfigOptions(antialias=True)

        self.showAxis('left', show=False)
        self.setLimits(xMin=Timeline.MIN_TIME)
        self.setRange(xRange=(-100, 10000))
        self.setRange(yRange=(-1, 1))
        self.getViewBox().setMouseEnabled(y=False)

        self.hitobjects_plot = HitobjectPlot()
        self.getPlotItem().addItem(self.hitobjects_plot, ignoreBounds=True)

        self.response_plot = LinePlot()
        self.getPlotItem().addItem(self.response_plot, ignoreBounds=True)

        self.timeline_marker = pyqtgraph.InfiniteLine(angle=90, movable=True)
        self.timeline_marker.setBounds((Timeline.MIN_TIME + 100, None))
        
        self.getPlotItem().addItem(self.timeline_marker, ignoreBounds=True)
        self.timeline_marker.sigPositionChanged.connect(self.time_changed_event)

        self.set_misc_data(None, None)


    def set_hitobject_data(self, hitobjects):
        data = [ (hitobject.time, hitobject.get_end_time()) for hitobject in hitobjects ]
        self.hitobjects_plot.update_data(data)


    def set_misc_data(self, data, mode):
        pass


    @callback
    def time_changed_event(self, marker):
        self.time_changed_event.emit(marker.value())
        