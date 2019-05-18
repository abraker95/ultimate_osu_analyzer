from misc.callback import callback


class Switcher():

    def __init__(self):
        self.data   = { None : None }
        self.active = None


    @callback
    def switch(self, key):
        if not key in self.data: 
            return False

        self.switch.emit(self.data[self.active], self.data[key], inst=self)
        self.active = key
        return True


    def __len__(self):
        return len(self.data)


    def get(self):
        return self.data[self.active]


    def add(self, key, data, overwrite=True):
        if key not in self.data or overwrite:
            self.data[key] = data
        else:
            raise Exception('Data with key "' + str(key) + '" already exists')


    # TODO: Figure out what is the best way to switch to another key
    def rmv(self, key):
        if key not in self.data: return
        if self.active == key:
            # Switch to first key if possible
            if len(self.data) > 1:
                self.switch(list(self.data.keys())[0])
            else:
                self.switch(None)

        del self.data[key]