from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph

from misc.callback import callback
from gui.objects.graph.line_graph import LineGraph
from analysis.map_metrics import MapMetrics



class TappingIntervalsGraph(LineGraph):

    MIN_TIME = -5000

    def __init__(self, hitobjects=None):
        super().__init__()
        self.update_graph_info(title='Tapping Intervals Graph', x_axis_label='Time (ms)', y_axis_label='Intervals (ms)')


    def get_data(self, hitobjects=None):
        if not hitobjects: return super().get_data()

        time                = MapMetrics.hitobject_start_times(hitobjects)
        hitobject_intervals = MapMetrics.calc_tapping_intervals(hitobjects)

        return time, hitobject_intervals