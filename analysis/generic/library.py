from analysis.generic.library_element import LibraryElement


class Library():

    def __init__(self):
        self.library = {}


    def add(self, name, elem):
        lib_elem = LibraryElement(name, elem)
        
        if not lib_elem.name in self.library:
            self.library[lib_elem.name] = lib_elem
        else:
            raise Exception('Library element ' + str(lib_elem.name) + ' already exists')


    def get(self, elem_name):
        return self.library[elem_name]


    def get_names(self):
        return list(self.library.keys())