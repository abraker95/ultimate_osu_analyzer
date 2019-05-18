from core.gamemode_manager import gamemode_manager


class Metric(object):

    def __init__(self, gamemode, name, inputs, outputs):
        self.name     = name
        self.inputs   = inputs
        self.outputs  = outputs
        self.gamemode = gamemode

        print('Metric "' + self.name + '" with ' + str(self.inputs) + ' inputs and ' + str(self.outputs) + ' outputs')


    def __call__(self, func):
        gamemode_manager.get_metric_lib(self.gamemode).add_metric(self.name, func)

        def wrap(*args, **kargs):
            return func(*args, **kargs)

        return wrap