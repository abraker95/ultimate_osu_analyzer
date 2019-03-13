from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.beatmap.beatmap_utility import BeatmapUtil
from misc.callback import callback

from gui.objects.layers.hitobject_outline_layer import HitobjectOutlineLayer
from gui.objects.layers.hitobject_aimpoint_layer import HitobjectAimpointLayer


'''
Visualizes a beatmap

Input: 
    beatmap - The beatmap to visualize
    time - The time value of the playfield. The time value which point in time to view the beatmap for.

Output: 
    Visual display of the beatmap's contents
'''
class Playfield(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)

        self.time = 0
        self.beatmap = None
        self.visible_hitobjects = []
        self.layers = {}

        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.set_time.connect(self.update_hitobject_visiblity)


    def load_beatmap(self, beatmap):
        self.beatmap = beatmap
        
        for hitobject in beatmap.hitobjects:
            #hitobject.setVisible(False)

            beatmap.set_cs_val.connect(hitobject.set_radius)
            #self.resizeEvent.connect(hitobject.set_ratios)
    
        beatmap.set_cs_val(beatmap.cs)

        self.create_basic_map_layers()
        

    def layer_changed(self):
        self.scene.update()


    #@callback
    def resizeEvent(self, event):
        for layer in self.layers.values():
            layer.area_resize_event(self.width(), self.height())

        self.scene.update()


    def update_hitobject_visiblity(self, time):
        print('time: ', time)

        self.visible_hitobjects = BeatmapUtil.get_hitobjects_visible_at_time(self.beatmap, time)
        for hitobject in self.visible_hitobjects:
            hitobject.time_changed(self.time)
            hitobject.set_opacity(BeatmapUtil.get_opacity_at(self.beatmap, hitobject, time))
            
        self.scene.update()


    @callback
    def set_time(self, time):        
        self.time = time
        self.set_time.emit(self.time)


    def get_layers(self):
        return self.layers.values()


    def get_layer(self, layer_name):
        return self.layers[layer_name]


    @callback
    def add_layer(self, layer):
        self.layers[layer.name] = layer
        self.scene.addItem(layer)
        self.scene.update()

        self.add_layer.emit(layer)


    def remove_layer(self, layer_name):
        self.scene.removeItem(self.layer[layer_name])
        del self.layer[layer_name]
        self.scene.update()


    def create_basic_map_layers(self):
        self.add_layer(HitobjectOutlineLayer(self))
        self.add_layer(HitobjectAimpointLayer(self))
        