from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from misc.math_utils import *

from osu.local.hitobject.mania.mania import Mania


class HitobjectRenderLayer(Layer, Temporal):

    def __init__(self, data, time_driver):
        Layer.__init__(self, 'Hitobject outlines')
        Temporal.__init__(self)

        self.beatmap = data
        
        # Drawing parameters
        self.viewable_time_interval = 1000   # ms
        self.note_width             = 50     # osu!px
        self.note_height            = 15     # osu!px
        self.note_seperation        = 5      # osu!px

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def set_viewable_time_interval(self, viewable_time_interval):
        self.viewable_time_interval = viewable_time_interval


    def paint(self, painter, option, widget):
        if not self.time: return

        ratio_x = widget.width()/Mania.PLAYFIELD_WIDTH    # px per osu!px
        ratio_y = widget.height()/Mania.PLAYFIELD_HEIGHT  # px per osu!px
        ratio_t = widget.height()/self.viewable_time_interval   # px per ms

        num_columns = int(self.beatmap.difficulty.cs)
        total_width = num_columns*(self.note_width + self.note_seperation)*ratio_x

        start_time = self.time
        end_time   = self.time + self.viewable_time_interval

        x_offset = widget.width()/2.0 - total_width/2.0
        y_offset = widget.height()

        draw_data = ratio_x, ratio_y, ratio_t, x_offset, y_offset, self.note_width, self.note_height, self.note_seperation

        for column in range(num_columns):
            start_idx = find(self.beatmap.hitobjects[column], start_time, selector=lambda hitobject: hitobject.time)
            end_idx   = find(self.beatmap.hitobjects[column], end_time,   selector=lambda hitobject: hitobject.get_end_time())
            
            visible_hitobjects = self.beatmap.hitobjects[column][start_idx : end_idx + 1]
            for visible_hitobject in visible_hitobjects:
                visible_hitobject.render_hitobject(painter, draw_data, self.time)