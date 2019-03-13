from gui.objects.layer import Layer
from osu.local.beatmap.beatmap_utility import *


class HitobjectAimpointLayer(Layer):

    def __init__(self, playfield):
        Layer.__init__(self, 'Hitobject aimpoints')
        self.playfield = playfield


    def area_resize_event(self, width, height):
        self.ratio_x = width/BeatmapUtil.PLAYFIELD_WIDTH
        self.ratio_y = height/BeatmapUtil.PLAYFIELD_HEIGHT


    def paint(self, painter, option, widget):
        for visible_hitobject in self.playfield.visible_hitobjects:
            try: visible_hitobject.render_hitobject_aimpoints(painter, self.ratio_x, self.ratio_y)
            except AttributeError: pass