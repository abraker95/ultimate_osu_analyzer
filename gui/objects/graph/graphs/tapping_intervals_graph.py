import pyqtgraph

from misc.callback import callback
from gui.objects.graph.line_graph import LineGraph
from analysis.map_metrics import MapMetrics



class TappingIntervalsGraph(LineGraph):

    MIN_TIME = -5000

    def __init__(self, hitobjects=None):
        super().__init__()
        self.update_graph_info(title='Tapping Intervals Graph', x_axis_label='Time (ms)', y_axis_label='Intervals (ms)')


    def hitobject_start_times(self, hitobjects):
        return [ hitobjects[i].time for i in range(1, len(hitobjects)) ]


    def get_data(self, hitobjects=None):
        if not hitobjects: return super().get_data()

        hitobject_start_times = self.hitobject_start_times(hitobjects)
        return MapMetrics.calc_tapping_intervals(hitobject_start_times)