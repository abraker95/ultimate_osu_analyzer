from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.objects.layer.layer import Layer
from osu.local.beatmap.beatmap_utility import *



class AimpointPathsLayer(Layer):

    def __init__(self, playfield):
        Layer.__init__(self, 'Aimpoint Paths')
        self.playfield = playfield


    def area_resize_event(self, width, height):
        self.ratio_x = width/BeatmapUtil.PLAYFIELD_WIDTH
        self.ratio_y = height/BeatmapUtil.PLAYFIELD_HEIGHT


    def aimpoint_positions(self):
        if len(self.playfield.visible_hitobjects) < 1: return

        hitobject_before_visible = self.playfield.beatmap.get_previous_hitobject(self.playfield.visible_hitobjects[0])
        if hitobject_before_visible: 
            try:
                time = hitobject_before_visible.get_aimpoints()[-1]
                yield hitobject_before_visible.time_to_pos(time)
            except AttributeError: pass

        for visible_hitobject in self.playfield.visible_hitobjects:
            try: 
                for aimpoint in visible_hitobject.get_aimpoints():
                    time = aimpoint
                    yield visible_hitobject.time_to_pos(time)
            except AttributeError: pass

        hitobject_after_visible = self.playfield.beatmap.get_next_hitobject(self.playfield.visible_hitobjects[-1])
        if hitobject_after_visible: 
            try:
                time = hitobject_after_visible.get_aimpoints()[0]
                yield hitobject_after_visible.time_to_pos(time)
            except AttributeError: pass 


    def paint(self, painter, option, widget):
        painter.setPen(QColor(255, 0, 0, 255))

        aimpoints = list(self.aimpoint_positions())
        for i in range(1, len(aimpoints)):
            prev_aimpoint, curr_aimpoint = aimpoints[i - 1], aimpoints[i]
            painter.drawLine(prev_aimpoint.x*self.ratio_x, prev_aimpoint.y*self.ratio_y, curr_aimpoint.x*self.ratio_x, curr_aimpoint.y*self.ratio_y)
