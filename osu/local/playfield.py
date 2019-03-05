from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.beatmap.beatmap_utility import BeatmapUtil
from misc.callback import callback


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

        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.scene = QGraphicsScene(self)
        #self.setMaximumSize(512, 384)
        self.setScene(self.scene)

        self.set_time.connect(self.update_hitobject_visiblity)


    def load_beatmap(self, beatmap):
        self.beatmap = beatmap
        
        for hitobject in beatmap.hitobjects:
            self.scene.addItem(hitobject)
            hitobject.setVisible(False)

            beatmap.set_cs_val.connect(hitobject.set_radius)
            self.resizeEvent.connect(hitobject.set_ratios)
    
        beatmap.set_cs_val(beatmap.cs)
        

    @callback
    def resizeEvent(self, event):
        self.resizeEvent.emit(self.width()/BeatmapUtil.PLAYFIELD_WIDTH, self.height()/BeatmapUtil.PLAYFIELD_HEIGHT)
        self.scene.update()


    def update_hitobject_visiblity(self, time):
        print('time: ', time)
        for hitobject in self.visible_hitobjects: 
            hitobject.setVisible(False)

        self.visible_hitobjects = BeatmapUtil.get_hitobjects_visible_at_time(self.beatmap, time)
        for hitobject in self.visible_hitobjects:
            hitobject.time_changed(self.time)
            hitobject.set_opacity(BeatmapUtil.get_opacity_at(self.beatmap, hitobject, time))
            hitobject.setVisible(True)
            
        self.scene.update()


    @callback
    def set_time(self, time):        
        self.time = time
        self.set_time.emit(self.time)
        