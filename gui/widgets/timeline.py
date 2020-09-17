from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph

from gui.objects.graph.hitobject_plot import HitobjectPlot
from gui.objects.graph.line_plot import LinePlot
from misc.callback import callback

from analysis.osu.std.map_data import StdMapData
from generic.switcher import Switcher


class Timeline(pyqtgraph.PlotWidget, Switcher):

    MIN_TIME = -5000

    def __init__(self):
        pyqtgraph.PlotWidget.__init__(self)
        Switcher.__init__(self)

        pyqtgraph.setConfigOptions(antialias=True)

        #self.showAxis('left', show=False)
        self.setLimits(xMin=Timeline.MIN_TIME)
        self.setRange(xRange=(-100, 10000))
        self.setRange(yRange=(-1, 1))
        self.getViewBox().setMouseEnabled(y=False)

        self.hitobjects_plot = HitobjectPlot([], [], [])
        self.getPlotItem().addItem(self.hitobjects_plot, ignoreBounds=True)

        self.response_plots = [ ]

        self.timeline_marker = pyqtgraph.InfiniteLine(angle=90, movable=True)
        self.timeline_marker.setBounds((Timeline.MIN_TIME + 100, None))
        
        self.getPlotItem().addItem(self.timeline_marker, ignoreBounds=True)
        self.timeline_marker.sigPositionChanged.connect(self.time_changed_event)

        self.y_mid_pos = 0


    def set_map(self, beatmap):
        if beatmap == None:
            self.hitobjects_plot.update_data([], [], [])
            return

        map_data = StdMapData.get_map_data(beatmap.hitobjects)
        self.hitobjects_plot.update_data(StdMapData.start_times(map_data), StdMapData.end_times(map_data), StdMapData.get_objects(map_data), y_pos=self.y_mid_pos)


    def save(self, name=None):
        if name == None:
            if not self.active: ValueError('Current switched value is None')
            else:               name = self.active

        data = {
            'view' : self.getPlotItem().viewRange(),
            'marker' : self.timeline_marker.value()
        }

        Switcher.add(self, name, data, overwrite=True)


    def load(self, name):
        if not self.switch(name): 
            raise ValueError('Nothing saved under the name %s' % name)
        
        data = self.get()

        self.setRange(xRange=data['view'][0])
        self.setRange(yRange=data['view'][1])
        self.timeline_marker.setValue(data['marker'])


    def set_misc_data(self, data):
        min_y = 0
        max_y = 0

        for response in data:
            response_plot = LinePlot()
            self.response_plots.append(response_plot)
            self.getPlotItem().addItem(response_plot, ignoreBounds=True)

            data_x, data_y = response
            max_y = max(max_y, max(data_y))
            min_y = min(min_y, min(data_y))

            response_plot.update_data(response)

        self.setRange(yRange=(min_y, max_y))

        y_mid_pos = (min_y + max_y)/2
        if self.y_mid_pos != y_mid_pos:
            self.y_mid_pos = y_mid_pos
            self.hitobjects_plot.update_data(self.hitobjects_plot.data, self.y_mid_pos)


    @callback
    def time_changed_event(self, marker):
        self.time_changed_event.emit(marker.value())
        