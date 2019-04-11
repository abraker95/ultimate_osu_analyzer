
class Metric():

    def __init__(self, func):
        self.func = func


    def get(self, *args, **kargs):
        return self.func(args, kargs)

