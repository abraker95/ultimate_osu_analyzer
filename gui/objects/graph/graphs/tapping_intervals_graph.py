from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph

from misc.callback import callback
from analysis.map_metrics import MapMetrics

class TappingIntervalsGraph(pyqtgraph.PlotWidget):

    MIN_TIME = -5000

    def __init__(self, hitobjects=None):
        super().__init__()
        pyqtgraph.setConfigOptions(antialias=True)

        self.showAxis('left', show=False)
        self.setLimits(xMin=TappingIntervalsGraph.MIN_TIME)
        self.setRange(xRange=(-100, 10000))

        self.getViewBox().setMouseEnabled(x=False, y=False)

        self.timeline_marker = pyqtgraph.InfiniteLine(angle=90, movable=True)
        self.timeline_marker.setBounds((TappingIntervalsGraph.MIN_TIME + 100, None))
        
        self.timeline_marker.sigPositionChanged.connect(self.time_changed_event)

        if hitobjects:
            self.plot(hitobjects)


    def plot(self, hitobjects):
        time                = MapMetrics.hitobject_start_times(hitobjects)
        hitobject_intervals = MapMetrics.calc_tapping_intervals(hitobjects)
        
        self.getPlotItem().plot(title="Tapping Intervals", x=time, y=hitobject_intervals, pen="r", clear=True)
        self.addItem(self.timeline_marker, ignoreBounds=True)
        
        self.setRange(xRange=(time[0] - 100, time[-1] + 100))
        self.setRange(yRange=(min(hitobject_intervals), max(hitobject_intervals)))


    def mouseDragEvent(self, event):
        event.ignore()


    @callback
    def time_changed_event(self, marker):
        self.time_changed_event.emit(marker.value())
        