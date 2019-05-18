from misc.callback import callback


class Temporal():

    def __init__(self):
        self.time = None


    @callback
    def time_changed(self, time):
        self.time = time
        self.time_changed.emit(time)