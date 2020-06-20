from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from pyqtgraph.dockarea import *

#from gui.widgets.temporal_hitobject_graph import TemporalHitobjectGraph
from gui.objects.graph.line_plot import LinePlot

from analysis.osu.std.map_metrics import StdMapMetrics



class GraphManager(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout    = QVBoxLayout()
        self.dock_area = QMainWindow()
        
        self.graphs = {}


        '''
        # TODO: 
            A scripting text field that allows to create new metrics to graph
            Default info avaliable:
                hitobjects ->
                    time
                    pos

            Ex:
                # Interval metrics
                x = [ hitobjects[i].time for i in range(1, len(hitobjects)) ]
                y = [ hitobjects[i].time - hitobjects[i - 1].time in range(1, len(hitobjects)) ]
        '''


    def construct_gui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.dock_area)


    def update_gui(self):
        self.dock_area.setCentralWidget(None)
        self.dock_area.setTabPosition(Qt.AllDockWidgetAreas, QTabWidget.North)
        self.dock_area.setDockNestingEnabled(True)


    def update_data(self):
        for graph in self.graphs.values():
            graph[0].update_data()


    def is_graph_exist(self, graph_name):
        return graph_name in self.graphs


    def get_num_graphs(self):
        return len(self.dock_area.findChildren(QDockWidget))


    def add_graph(self, graph):
        print('Adding graph for ' + str(graph.getPlotItem().titleLabel.text))

        # TODO: Handle closing of floating docks
        dock = QDockWidget(graph.getPlotItem().titleLabel.text, self)
        dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        dock.setWidget(graph)

        self.dock_area.addDockWidget(Qt.LeftDockWidgetArea, dock)           # I have no idea why Left/Right is reversed
        self.graphs[graph.getPlotItem().titleLabel.text] = [ graph, dock ]

    
    '''
    def add_graph_for_metric(self, metric, plot_type=None):
        number_dimensions = metric.get_metric_dimensions()

        # Validate and/or choose plot type
        if plot_type != None:
            if not plot_type.accepts_dim(number_dimensions):
                raise Exception('Plot type indicated cannot accept ' + str(number_dimensions) + ' dimensions')
        else:
            if    number_dimensions == 1: return  # TODO
            elif  number_dimensions == 2: plot_type = LinePlot()
            elif  number_dimensions == 3: return  # TODO
            elif  number_dimensions == 4: return  # TODO
            else: return  # TODO: Unsupported?

        # TODO: Support for other types of graphs that are not time related
        self.add_graph(TemporalHitobjectGraph(plot_type, metric.name, metric))
    '''

            
    def remove_graph(self, graph_name):
        self.dock_area.removeDockWidget(self.graphs[graph_name][1])
        del self.graphs[graph_name]

    
    def clear(self):
        for dock in self.graphs.values():
            dock[1].setParent(None)
        self.graphs = {}


