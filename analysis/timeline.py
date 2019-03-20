from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph

from misc.callback import callback


class Timeline(pyqtgraph.PlotWidget):

    MIN_TIME = -5000

    def __init__(self):
        super().__init__()
        pyqtgraph.setConfigOptions(antialias=True)

        self.showAxis('left', show=False)
        self.setLimits(xMin=Timeline.MIN_TIME)
        self.setRange(xRange=(-100, 10000))

        self.timeline_marker = pyqtgraph.InfiniteLine(angle=90, movable=True)
        self.timeline_marker.setBounds((Timeline.MIN_TIME + 100, None))
        
        self.addItem(self.timeline_marker, ignoreBounds=True)        
        self.timeline_marker.sigPositionChanged.connect(self.time_changed_event)


    @callback
    def time_changed_event(self, marker):
        self.time_changed_event.emit(marker.value())
        