from gui.objects.group import Group
from gui.objects.scene import Scene

from misc.callback import callback


class LayerManager(Group, Scene):

    def __init__(self):
        Group.__init__(self, 'root', self)
        Scene.__init__(self)


    @callback
    def add_layer(self, layer_name, layer, path=None):
        if not path: group = self
        else:
            names = path.split('.')
            group = self.child(names[0])

            for name in names[1:]:
                group = self.child(name)

        group.add_elem(layer_name, layer)
        Scene.add_layer(self, layer)

        self.add_layer.emit(layer, inst=self)


    @callback
    def rmv_layer(self, layer_name, path=None):
        if not path: group = self
        else:
            names = path.split('.')
            group = self.child(names[0])

            for name in names[1:]:
                group = group.child(name)

        layer = group.child(layer_name)
        Scene.rmv_layer(self, layer)
        group.rmv_elem(name)

        self.rmv_layer.emit(layer, inst=self)