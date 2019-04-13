import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.graph_manager import GraphManager
from gui.widgets.temporal_hitobject_graph import TemporalHitobjectGraph
from gui.objects.graph.line_plot import LinePlot

from analysis.osu.std.map_metrics import MapMetrics


class GraphManagerTest(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        
        self.graph_manager = GraphManager()
        self.setCentralWidget(self.graph_manager)

        self.setWindowTitle('Graph manager test')
        self.show()


    def run_tests(self, app):
        self.add_remove_graph_test(app)
        time.sleep(1)
        self.remove_graph_failure_test(app)
        time.sleep(1)
        self.multi_add_remove_graph_test(app)
        time.sleep(1)
        self.clear_graphs_test(app)
        time.sleep(1)
        self.multi_time_minupilation(app)
        time.sleep(1)
        self.multi_time_minupilation_add_remove(app)
        time.sleep(1)


    '''
    General Graph Tests
    '''
    def add_remove_graph_test(self, app):
        print('add_remove_graph_test')
        temporal_graph = TemporalHitobjectGraph(LinePlot(), 'test', lambda: None)
        self.graph_manager.add_graph(temporal_graph)
        time.sleep(0.1)
        app.processEvents()

        assert self.graph_manager.is_graph_exist('test'), 'Graph "test" does not exist'
        assert self.graph_manager.get_num_graphs() == 1, 'Number of graphs managed by graph manager is not 1; %s graphs exist' % str(self.graph_manager.get_num_graphs())
        
        self.graph_manager.remove_graph('test')
        time.sleep(0.1)
        app.processEvents()

        assert not self.graph_manager.is_graph_exist('test'), 'Graph "test" still exists'
        assert self.graph_manager.get_num_graphs() == 0, 'Number of graphs managed by graph manager is not 0; %s graphs exist' % str(self.graph_manager.get_num_graphs())

        print('\tTest passed')
        return True

    
    def multi_add_remove_graph_test(self, app):
        print('multi_add_remove_graph_test')
        for i in range(10):
            temporal_graph = TemporalHitobjectGraph(LinePlot(), 'test' + str(i), lambda: None)
            self.graph_manager.add_graph(temporal_graph)
            time.sleep(0.1)
            app.processEvents()

        assert self.graph_manager.get_num_graphs() == 10, 'Number of graphs managed by graph manager is not 10; %s graphs exist' % str(self.graph_manager.get_num_graphs())
        for i in range(10):
            assert self.graph_manager.is_graph_exist('test' + str(i)), 'Graph "%s" does not exist' % ('test' + str(i))        

        for i in range(10):
            self.graph_manager.remove_graph('test' + str(i))
            time.sleep(0.1)
            app.processEvents()

        assert self.graph_manager.get_num_graphs() == 0, 'Number of graphs managed by graph manager is not 0; %s graphs exist' % str(self.graph_manager.get_num_graphs())
        for i in range(10):
            assert not self.graph_manager.is_graph_exist('test' + str(i)), 'Graph "%s" exists' % ('test' + str(i))

        print('\tTest passed')
        return True
        

    def remove_graph_failure_test(self, app):
        print('remove_graph_failure_test')
        temporal_graph = TemporalHitobjectGraph(LinePlot(), 'test', lambda: None)
        self.graph_manager.add_graph(temporal_graph)
        app.processEvents()
        time.sleep

        try: self.graph_manager.remove_graph('AAA')
        except KeyError as e: pass
        else: assert False, 'Removing graph "AAA" should have failed'
        
        assert self.graph_manager.get_num_graphs() == 1, 'Number of graphs managed by graph manager is not 1; %s graphs exist' % str(self.graph_manager.get_num_graphs())
        assert self.graph_manager.is_graph_exist('test'), 'Graph "test" does not exists'
        
        try: self.graph_manager.remove_graph('test')
        except KeyError as e: assert False, 'Removing graph "test" should have succeeded'
        time.sleep(0.1)
        app.processEvents()

        assert self.graph_manager.get_num_graphs() == 0, 'Number of graphs managed by graph manager is not 0; %s graphs exist' % str(self.graph_manager.get_num_graphs())
        assert not self.graph_manager.is_graph_exist('test'), 'Graph "test" exists'

        print('\tTest passed')
        return True

    
    def clear_graphs_test(self, app):
        print('clear_graphs_test')
        for i in range(10):
            temporal_graph = TemporalHitobjectGraph(LinePlot(), 'test' + str(i), lambda: None)
            self.graph_manager.add_graph(temporal_graph)
            time.sleep(0.1)
            app.processEvents()
        
        assert self.graph_manager.get_num_graphs() == 10, 'Number of graphs managed by graph manager is not 10; %s graphs exist' % str(self.graph_manager.get_num_graphs())

        self.graph_manager.clear()
        time.sleep(0.1)
        app.processEvents()

        assert self.graph_manager.get_num_graphs() == 0, 'Number of graphs managed by graph manager is not 0; %s graphs exist' % str(self.graph_manager.get_num_graphs())

        # TODO: How to check whether a dock still exists as a window?
        print('\tTest passed')
        return True


    '''
    Specific Graph Interaction Tests
    '''
    def multi_time_minupilation(self, app):
        print('multi_time_minupilation')

        # Test them both connected
        temporal_graph_1 = TemporalHitobjectGraph(LinePlot(), 'test_1', lambda: None)
        self.graph_manager.add_graph(temporal_graph_1)

        temporal_graph_2 = TemporalHitobjectGraph(LinePlot(), 'test_2', lambda: None)
        self.graph_manager.add_graph(temporal_graph_2)

        TemporalHitobjectGraph.time_changed_event.connect(temporal_graph_2.timeline_marker.setValue)
        TemporalHitobjectGraph.time_changed_event.connect(temporal_graph_1.timeline_marker.setValue)

        for t in range(1, 2000, 10):
            temporal_graph_1.timeline_marker.setValue(t)
            time.sleep(0.01)
            app.processEvents()

            graph_1_time = temporal_graph_1.timeline_marker.value()
            graph_2_time = temporal_graph_2.timeline_marker.value()
            assert graph_1_time == graph_2_time, 'Graph time markers do not match'

        # Disconnect and move each graphs' marker
        TemporalHitobjectGraph.time_changed_event.disconnect(temporal_graph_2.timeline_marker.setValue)
        TemporalHitobjectGraph.time_changed_event.disconnect(temporal_graph_1.timeline_marker.setValue)

        for t in range(2001, 4000, 10):
            temporal_graph_1.timeline_marker.setValue(t)
            time.sleep(0.01)
            app.processEvents()

            graph_1_time = temporal_graph_1.timeline_marker.value()
            graph_2_time = temporal_graph_2.timeline_marker.value()
            assert graph_1_time != graph_2_time, 'Moving temporal graph 1 marker; Graph time markers match'

        for t in range(0, 2000, 10):
            temporal_graph_2.timeline_marker.setValue(t)
            time.sleep(0.01)
            app.processEvents()

            graph_1_time = temporal_graph_1.timeline_marker.value()
            graph_2_time = temporal_graph_2.timeline_marker.value()
            assert graph_1_time != graph_2_time, 'Moving temporal graph 2 marker; Graph time markers match'

        self.graph_manager.clear()
        app.processEvents()

        print('\tTest passed')
        return True


    def multi_time_minupilation_add_remove(self, app):
        print('multi_time_minupilation_add_remove')
        
        # Create a bunch of graphs and connect their markers
        graphs = {}
        for i in range(5):
            graph = TemporalHitobjectGraph(LinePlot(), 'test' + str(i), lambda: None)
            self.graph_manager.add_graph(graph)
            graphs['test' + str(i)] = graph

        for graph in graphs.values():
            TemporalHitobjectGraph.time_changed_event.connect(graph.timeline_marker.setValue)
 
        # Move the marker of each graph, one by one
        for graph in graphs.values():
            for t in range(0, 3000, 15):
                graph.timeline_marker.setValue(t)

                for other_graph in graphs.values():
                    if other_graph == graph: continue

                    graph_time = graph.timeline_marker.value()
                    other_graph_time = other_graph.timeline_marker.value()
                    assert graph_time == other_graph_time, 'Graph time markers do not match; (%s:%i == %s:%i)' % (graph.get_name(), graph_time, other_graph.get_name(), other_graph_time)

                time.sleep(0.01)
                app.processEvents()

        # Remove a few graphs
        remove_graphs = [ 'test1', 'test4' ]
        for name in remove_graphs:
            TemporalHitobjectGraph.time_changed_event.disconnect(graphs[name].timeline_marker.setValue)

            self.graph_manager.remove_graph(name)
            del graphs[name]

            time.sleep(0.1)
            app.processEvents()

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
                    
                    if other_graph.get_name() in remove_graphs: assert graph_time != other_graph_time, 'Removed graph time marker matches; (%s:%i == %s:%i)' % (graph.get_name(), graph_time, other_graph.get_name(), other_graph_time)
                    if other_graph.get_name() not in remove_graphs: assert graph_time == other_graph_time, 'Kept time marker does not match; (%s:%i != %s:%i)' % (graph.get_name(), graph_time, other_graph.get_name(), other_graph_time)

                time.sleep(0.01)
                app.processEvents()

        self.graph_manager.clear()

        print('\tTest passed')
        return True