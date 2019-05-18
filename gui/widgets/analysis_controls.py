from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.callback import callback

from gui.widgets.QContainer import QContainer
from gui.widgets.dockable_graph import DockableGraph
from gui.widgets.temporal_hitobject_graph import TemporalHitobjectGraph

from gui.objects.graph.line_plot import LinePlot

#from analysis.metrics.metric_library_proxy import MetricLibraryProxy
from core.gamemode_manager import gamemode_manager
from core.graph_manager import graph_manager


class DropdownItem(QWidget):

    def __init__(self, label_text):
        super().__init__()

        self.layout   = QHBoxLayout()
        self.label    = QLabel(label_text)
        self.dropdown = QComboBox()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dropdown)
        self.setLayout(self.layout)

        self.set_dropdown([])


    def set_dropdown(self, dropdown_items):
        for i in range(self.dropdown.count()):
            self.dropdown.removeItem(i)

        self.dropdown.addItems(dropdown_items)


    def remove_item(self, idx):
        self.dropdown.removeItem(idx)


    def count(self):
        return self.dropdown.count()


    def connect_select_event(self, callback):
        self.dropdown.activated.connect(callback)



class MetricOption(DropdownItem):

    def __init__(self, option_num):
        super().__init__('Metric ' + str(option_num) + ': ')
        self.option_num = option_num
        self.refresh_metrics()


    def refresh_metrics(self):
        for i in range(self.dropdown.count()):
            self.dropdown.removeItem(i)

        metric_library = MetricLibraryProxy.proxy.get_active_lib()
        if not metric_library: return

        # TODO: Fix
        #self.dropdown.addItems(gamemode_manager.get().get_names())
            


class AnalysisControls(QWidget):

    def __init__(self):
        super().__init__()

        self.selected_graph_type = None
        self.selected_plot_type  = None

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.main_layout = QVBoxLayout()

        self.label = QLabel('Analysis Controls')
        self.metric_options = []

        self.metric_options_container = QContainer(QVBoxLayout())
        self.metric_btn_container     = QContainer(QHBoxLayout())
        self.add_metric_btn           = QPushButton('+ add')
        self.rmv_metric_btn           = QPushButton('- rmv')

        self.graph_type_selection = DropdownItem('Graph Type: ')
        self.plot_type_selection  = DropdownItem('Plot Type: ')
        
        self.create_graph_btn = QPushButton('Create Graph')
      

    def construct_gui(self):
        self.main_layout.addWidget(self.metric_options_container)
        self.main_layout.addWidget(self.metric_btn_container)
        self.main_layout.addWidget(self.graph_type_selection)
        self.main_layout.addWidget(self.plot_type_selection)
        self.main_layout.addWidget(self.create_graph_btn)
        
        self.metric_btn_container.addWidget(self.add_metric_btn)
        self.metric_btn_container.addWidget(self.rmv_metric_btn)

        self.setLayout(self.main_layout)


    def update_gui(self):
        self.label.setAlignment(Qt.AlignCenter)

        self.graph_type_selection.connect_select_event(self.__graph_type_select_event)
        self.plot_type_selection.connect_select_event(self.__plot_type_select_event)
        self.add_metric_btn.clicked.connect(self.__add_metric_event)
        self.rmv_metric_btn.clicked.connect(self.__rmv_metric_event)
        self.create_graph_btn.clicked.connect(self.create_graph_event)


    def __add_metric_event(self):
        metric_option = MetricOption(len(self.metric_options))
        self.metric_options.append(metric_option)
        self.metric_options_container.addWidget(metric_option)

        self.refresh_allowable_graph_types()


    def __rmv_metric_event(self):
        if len(self.metric_options) == 0: return

        self.metric_options[-1].setParent(None)
        self.metric_options.remove(self.metric_options[-1])


    def refresh_metrics(self):
        for metric_option in self.metric_options:
            metric_option.refresh_metrics()


    def refresh_allowable_graph_types(self):
        for i in range(self.graph_type_selection.count()):
            self.graph_type_selection.remove_item(i)

        # TODO: Add the ones only supported by the number of metrics there are
        self.graph_type_selection.set_dropdown(graph_types.get_names())
        self.selected_graph_type = self.graph_type_selection.dropdown.currentText()


    def __graph_type_select_event(self, index):
        self.selected_graph_type = self.graph_type_selection.dropdown.currentText()
        # TODO: self.plot_type_selection.set_dropdown(self, plot_types)


    def __plot_type_select_event(self, index):
        self.selected_plot_type = self.plot_type_selection.dropdown.currentText()


    @callback
    def create_graph_event(self, _):
        if self.selected_graph_type == 'temporal_hitobject_graph':
            #dockable_graph = DockableGraph(TemporalHitobjectGraph(LinePlot(), 'test', lambda: 0))
            #dockable_graph.show()

            self.create_graph_event.emit(TemporalHitobjectGraph(LinePlot(), 'test', lambda: 0))