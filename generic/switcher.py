from misc.callback import callback


class Switcher():

    def __init__(self):
        self.data = {}
        self.active = None


    @callback
    def switch(self, name):
        self.active = self.data[name]
        Switcher.switch.emit(self.active, inst=self)


    def __len__(self):
        return len(self.data)


    def get(self):
        return self.active


    def add(self, name, data):
        if name not in self.data:
            self.data[name] = data
        else:
            raise Exception('Data with name "' + str(name) + '" already exists')

    
    def rmv(self, name):
        if name not in self.data: return
        del self.data[name]