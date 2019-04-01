from collections import OrderedDict
import pyqtgraph

from misc.callback import callback
from gui.objects.graph.line_graph import LineGraph
from analysis.map_metrics import MapMetrics



class VelocityGraph(LineGraph):

    MIN_TIME = -5000

    def __init__(self, hitobjects=None):
        super().__init__()
        self.update_graph_info(title='Velocity Graph', x_axis_label='Time (ms)', y_axis_label='Velocity (ms/px)')


    def get_aimpoints(self, hitobjects):
        aimpoints = []
        for hitobject in hitobjects:
            try:
                for aimpoint in hitobject.get_aimpoints():
                    aimpoints.append( (aimpoint, hitobject.time_to_pos(aimpoint)) )
            except AttributeError: pass

        return sorted(aimpoints, key=lambda aimpoint: aimpoint[0])


    def get_data(self, hitobjects=None):
        if not hitobjects: return super().get_data()

        aimpoints = self.get_aimpoints(hitobjects)
        if len(aimpoints) < 1: return ( [], [] )

        return MapMetrics.calc_velocity(aimpoints)