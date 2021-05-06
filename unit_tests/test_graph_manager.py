import unittest
import time
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.graph_manager import GraphManager
from gui.widgets.data_2d_graph import Data2DGraph
from gui.objects.graph.line_plot import LinePlot



class TestGraphManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
        cls.win = QMainWindow()
        
        cls.graph_manager = GraphManager()
        cls.win.setCentralWidget(cls.graph_manager)

        cls.win.setWindowTitle('Graph manager test')
        cls.win.show()


    @classmethod
    def tearDown(cls):  
        time.sleep(1)


    """
    General Graph Tests
    """
    def test_add_remove_graph(self):
        temporal_graph = Data2DGraph('test', np.asarray([[0], [0]]), temporal=True)
        self.graph_manager.add_graph(temporal_graph)
        time.sleep(0.1)
        self.app.processEvents()

        self.assertTrue(self.graph_manager.is_graph_exist('test'),  'Graph "test" does not exist')
        self.assertEqual(self.graph_manager.get_num_graphs(), 1, f'Number of graphs managed by graph manager is not 1; {self.graph_manager.get_num_graphs()} graphs exist')
        
        self.graph_manager.remove_graph('test')
        time.sleep(0.1)
        self.app.processEvents()

        self.assertFalse(self.graph_manager.is_graph_exist('test'),  'Graph "test" still exists')
        self.assertEqual(self.graph_manager.get_num_graphs(), 0, f'Number of graphs managed by graph manager is not 0; {self.graph_manager.get_num_graphs()} graphs exist')


    def test_multi_add_remove_graph(self):
        for i in range(10):
            temporal_graph = Data2DGraph(f'test {i}', np.asarray([[0], [0]]), temporal=True)
            self.graph_manager.add_graph(temporal_graph)
            time.sleep(0.1)
            self.app.processEvents()

        self.assertEqual(self.graph_manager.get_num_graphs(), 10, f'Number of graphs managed by graph manager is not 10; {self.graph_manager.get_num_graphs()} graphs exist')
        for i in range(10):
            self.assertTrue(self.graph_manager.is_graph_exist(f'test {i}'), f'Graph "test {i}" does not exist')

        for i in range(10):
            self.graph_manager.remove_graph(f'test {i}')
            time.sleep(0.1)
            self.app.processEvents()

        self.assertEqual(self.graph_manager.get_num_graphs(), 0, f'Number of graphs managed by graph manager is not 0; {self.graph_manager.get_num_graphs()} graphs exist')
        for i in range(10):
            self.assertFalse(self.graph_manager.is_graph_exist(f'test {i}'), f'Graph "test {i}" exists')


    def test_remove_graph_failure(self):
        temporal_graph = Data2DGraph('test', np.asarray([[0], [0]]), temporal=True)
        self.graph_manager.add_graph(temporal_graph)
        time.sleep(0.1)
        self.app.processEvents()

        self.assertRaises(KeyError, self.graph_manager.remove_graph, 'AAA')
        
        self.assertEqual(self.graph_manager.get_num_graphs(), 1, f'Number of graphs managed by graph manager is not 1; {self.graph_manager.get_num_graphs()} graphs exist')
        self.assertTrue(self.graph_manager.is_graph_exist('test'),  'Graph "test" does not exist')
        
        try: self.graph_manager.remove_graph('test')
        except KeyError: self.fail('Removing graph "test" should have succeeded')

        time.sleep(0.1)
        self.app.processEvents()

        self.assertFalse(self.graph_manager.is_graph_exist('test'),  'Graph "test" still exists')
        self.assertEqual(self.graph_manager.get_num_graphs(), 0, f'Number of graphs managed by graph manager is not 0; {self.graph_manager.get_num_graphs()} graphs exist')


    def test_clear_graphs(self):
        for i in range(10):
            temporal_graph = Data2DGraph(f'test {i}', np.asarray([[0], [0]]), temporal=True)
            self.graph_manager.add_graph(temporal_graph)
            time.sleep(0.1)
            self.app.processEvents()
        
        self.assertEqual(self.graph_manager.get_num_graphs(), 10, f'Number of graphs managed by graph manager is not 10; {self.graph_manager.get_num_graphs()} graphs exist')

        self.graph_manager.clear()
        time.sleep(0.1)
        self.app.processEvents()

        self.assertEqual(self.graph_manager.get_num_graphs(), 0, f'Number of graphs managed by graph manager is not 0; {self.graph_manager.get_num_graphs()} graphs exist')

        # TODO: How to check whether a dock still exists as a window?


    """
    Specific Graph Interaction Tests
    """
    def test_multi_time_minupilation(self):
        # Test them both connected
        temporal_graph_1 = Data2DGraph('test', np.asarray([[0], [0]]), temporal=True)
        self.graph_manager.add_graph(temporal_graph_1)

        temporal_graph_2 = Data2DGraph('test', np.asarray([[0], [0]]), temporal=True)
        self.graph_manager.add_graph(temporal_graph_2)

        Data2DGraph.time_changed_event.connect(temporal_graph_2.timeline_marker.setValue)
        Data2DGraph.time_changed_event.connect(temporal_graph_1.timeline_marker.setValue)

        for t in range(1, 2000, 10):
            temporal_graph_1.timeline_marker.setValue(t)
            time.sleep(0.01)
            self.app.processEvents()

            graph_1_time = temporal_graph_1.timeline_marker.value()
            graph_2_time = temporal_graph_2.timeline_marker.value()
            self.assertEqual(graph_1_time, graph_2_time, 'Graph time markers do not match')

        # Disconnect and move each graphs' marker
        Data2DGraph.time_changed_event.disconnect(temporal_graph_2.timeline_marker.setValue)
        Data2DGraph.time_changed_event.disconnect(temporal_graph_1.timeline_marker.setValue)

        for t in range(2001, 4000, 10):
            temporal_graph_1.timeline_marker.setValue(t)
            time.sleep(0.01)
            self.app.processEvents()

            graph_1_time = temporal_graph_1.timeline_marker.value()
            graph_2_time = temporal_graph_2.timeline_marker.value()
            self.assertNotEqual(graph_1_time, graph_2_time, 'Moving temporal graph 1 marker; Graph time markers match')

        for t in range(0, 2000, 10):
            temporal_graph_2.timeline_marker.setValue(t)
            time.sleep(0.01)
            self.app.processEvents()

            graph_1_time = temporal_graph_1.timeline_marker.value()
            graph_2_time = temporal_graph_2.timeline_marker.value()
            self.assertNotEqual(graph_1_time, graph_2_time, 'Moving temporal graph 2 marker; Graph time markers match')

        self.graph_manager.clear()
        self.app.processEvents()


    def test_multi_time_minupilation_add_remove(self):
        # Create a bunch of graphs and connect their markers
        graphs = {}
        for i in range(5):
            graph = Data2DGraph(f'test {i}', np.asarray([[0], [0]]), temporal=True)
            self.graph_manager.add_graph(graph)
            graphs[f'test {i}'] = graph

        for graph in graphs.values():
            Data2DGraph.time_changed_event.connect(graph.timeline_marker.setValue)
 
        # Move the marker of each graph, one by one
        for graph in graphs.values():
            for t in range(0, 3000, 15):
                graph.timeline_marker.setValue(t)

                for other_graph in graphs.values():
                    if other_graph == graph: continue

                    graph_time = graph.timeline_marker.value()
                    other_graph_time = other_graph.timeline_marker.value()
                    self.assertEqual(graph_time, other_graph_time, f'Graph time markers do not match; ({graph.get_name()}:{graph_time} == {other_graph.get_name()}:{other_graph_time})')

                time.sleep(0.01)
                self.app.processEvents()

        # Remove a few graphs
        remove_graphs = [ 'test 1', 'test 4' ]
        for name in remove_graphs:
            Data2DGraph.time_changed_event.disconnect(graphs[name].timeline_marker.setValue)

            self.graph_manager.remove_graph(name)
            del graphs[name]

            time.sleep(0.1)
            self.app.processEvents()

        # Move the markers, ensuring no exceptions arise due to removed/deleted graphs
        for graph in graphs.values():
            for t in range(0, 2000, 10):
                # Let first graph be one that has not been removed
                if graph.get_name() in remove_graphs: continue
                    
                graph.timeline_marker.setValue(t)

                for other_graph in graphs.values():
                    # Skip if it's same graph
                    if other_graph == graph: continue

                    graph_time = graph.timeline_marker.value()
                    other_graph_time = other_graph.timeline_marker.value()
                    
                    if other_graph.get_name() in remove_graphs: self.assertNotEqual(graph_time, other_graph_time, 'Removed graph time marker matches; ({graph.get_name()}:{graph_time} == {other_graph.get_name()}:{other_graph_time})')
                    if other_graph.get_name() not in remove_graphs: self.assertEqual(graph_time, other_graph_time, 'Kept time marker does not match; ({graph.get_name()}:{graph_time} == {other_graph.get_name()}:{other_graph_time})')

                time.sleep(0.01)
                self.app.processEvents()

        self.graph_manager.clear()