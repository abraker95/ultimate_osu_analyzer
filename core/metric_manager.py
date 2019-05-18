from misc.callback import callback
from gui.objects.group import Group


class MetricManager(Group):

    def __init__(self):
        Group.__init__(self, 'root', self)


    @callback
    def add_metric(self, metric_name, metric, path=None):
        if not path: group = self
        else:
            names = path.split('.')
            group = self.child(names[0])

            for name in names[1:]:
                group = self.child(name)

        group.add_elem(metric_name, metric)


    @callback
    def rmv_metric(self, metric_name, path=None):
        if not path: group = self
        else:
            names = path.split('.')
            group = self.child(names[0])

            for name in names[1:]:
                group = group.child(name)

        group.rmv_elem(metric_name)