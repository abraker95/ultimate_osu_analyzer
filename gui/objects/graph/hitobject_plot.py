import pyqtgraph
import numpy as np
from pyqtgraph import QtCore, QtGui


class HitobjectPlot(pyqtgraph.GraphItem):

    HITOBJECT_RADIUS = 40

    def __init__(self, data=None):
        pyqtgraph.GraphItem.__init__(self)
        pyqtgraph.setConfigOptions(antialias=True)

        self.pen = pyqtgraph.mkPen(width=HitobjectPlot.HITOBJECT_RADIUS)
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.setPen(self.pen)
    

    def update_data(self, data):
        pos  = []
        adj  = []
        size = []

        obj_num = -1

        for (time_start, time_end) in data:
            pos.append([ time_start, 0 ])
            size.append(HitobjectPlot.HITOBJECT_RADIUS)
            obj_num += 1

            # Slider end
            if time_start != time_end:
                pos.append([ time_end, 0 ])
                size.append(0)
                obj_num += 1

                adj.append([ obj_num - 1, obj_num ])

        pos = np.array(pos, dtype=np.int)
        adj = np.array(adj, dtype=np.int)

        self.setData(pos=pos, adj=adj, size=size, symbol='o', pxMode=True)