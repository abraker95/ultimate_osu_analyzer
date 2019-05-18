from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class DockableGraph(QDockWidget):

    def __init__(self, graph, floating=True):
        super().__init__(graph.getPlotItem().titleLabel.text)

        self.graph = graph

        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setWidget(graph)

        self.setFloating(floating)