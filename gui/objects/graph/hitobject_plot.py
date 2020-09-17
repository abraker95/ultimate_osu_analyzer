import pyqtgraph
import numpy as np
from pyqtgraph import QtCore, QtGui

from analysis.osu.std.map_data import StdMapData


class HitobjectPlot(pyqtgraph.GraphItem):

    HITOBJECT_RADIUS = 40

    def __init__(self, start_times, end_times, h_types, y_pos=0):
        pyqtgraph.GraphItem.__init__(self)
        pyqtgraph.setConfigOptions(antialias=True)

        self.pen = pyqtgraph.mkPen(width=HitobjectPlot.HITOBJECT_RADIUS)
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.setPen(self.pen)

        self.update_data(start_times, end_times, h_types, y_pos)
    

    def update_data(self, start_times, end_times, h_types, y_pos=0):
        try:
            if len(start_times) == 0 or len(end_times) == 0 or len(h_types) == 0:
                self.scatter.clear()
                self.pos = None
                return
        except ValueError: return

        pos  = []
        adj  = []
        size = []

        obj_num = -1

        for start_time, end_time, h_type in zip(start_times, end_times, h_types):
            pos.append([ start_time, y_pos ])
            size.append(HitobjectPlot.HITOBJECT_RADIUS)
            obj_num += 1

            # Slider end
            if h_type == StdMapData.TYPE_SLIDER:
                pos.append([ end_time, y_pos ])
                size.append(0)
                obj_num += 1

                adj.append([ obj_num - 1, obj_num ])
            else:
                adj.append([ obj_num, obj_num ])

        pos = np.array(pos, dtype=np.float)
        adj = np.array(adj, dtype=np.int)

        self.setData(pos=pos, adj=adj, size=size, symbol='o', pxMode=True)