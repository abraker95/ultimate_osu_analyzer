

class LibraryElement():

    def __init__(self, name, elem):
        self.name = name
        self.elem = elem


    def get(self):
        '''
        self.elem can be anything, function or object, etc
        This self.get() needs to be extended to allow interfacing with self.elem through LibraryElement
        '''
        raise NotImplementedError()
