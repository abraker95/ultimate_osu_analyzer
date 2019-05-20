from misc.callback import callback


class Group():

    def __init__(self, name, parent):
        self.parent = parent
        self.name   = name
        self.data   = {}


    def __len__(self):
        return len(self.data)


    @callback
    def add_group(self, name):
        if name in self.data: return
        self.data[name] = Group(name, self)

        Group.add_group.emit(self.data[name])


    @callback
    def rmv_group(self, name):
        if not name in self.data: return
        
        Group.rmv_group.emit(self.data[name])
        del self.data[name]


    @callback
    def add_elem(self, name, elem):
        if name in self.data: return
        self.data[name] = elem

        Group.add_elem.emit(self, elem)


    @callback
    def rmv_elem(self, name):
        if not name in self.data: return
        
        Group.rmv_elem.emit(self, self.data[name])
        del self.data[name]


    def child(self, name):
        return self.data[name]


    def get_structure(self):
        structure = {}
        for name, data in self.data.items():
            try:    structure[name] = data.get_structure()
            except: structure[name] = type(data)

        return structure