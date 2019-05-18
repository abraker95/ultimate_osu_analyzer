from misc.callback import callback
from gui.objects.group import Group


class GraphManager(Group):

    def __init__(self):
        Group.__init__(self, 'root', self)


    @callback
    def add_graph(self, graph_name, graph):
        self.add_elem(graph_name, graph)


    @callback
    def rmv_graph(self, graph_name):
        self.rmv_elem(graph_name)


graph_manager = GraphManager()