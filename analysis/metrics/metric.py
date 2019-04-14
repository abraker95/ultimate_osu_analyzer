from analysis.metrics.metric_library_proxy import MetricLibraryProxy


class Metric(object):

    def __init__(self, gamemode, name, inputs, outputs):
        self.name     = name
        self.inputs   = inputs
        self.outputs  = outputs
        self.gamemode = gamemode

        print('Metric "' + self.name + '" with ' + str(self.inputs) + ' inputs and ' + str(self.outputs) + ' outputs')


    def __call__(self, func):
        MetricLibraryProxy.proxy.get_metric_lib(self.gamemode).add(self.name, func)

        def wrap(*args, **kargs):
            return func(*args, **kargs)

        return wrap