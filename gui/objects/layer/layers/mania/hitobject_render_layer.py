from generic.temporal import Temporal
from gui.objects.layer.layer import Layer
from misc.math_utils import *

from osu.local.hitobject.mania.mania import Mania, ManiaSettings


class HitobjectRenderLayer(Layer, Temporal):

    def __init__(self, data, time_driver):
        Layer.__init__(self, 'Hitobject render')
        Temporal.__init__(self)

        self.beatmap = data

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())

        ManiaSettings.set_note_height.connect(self.layer_changed)
        ManiaSettings.set_note_width.connect(self.layer_changed)
        ManiaSettings.set_note_seperation.connect(self.layer_changed)
        ManiaSettings.set_viewable_time_interval.connect(self.layer_changed)


    def paint(self, painter, option, widget):
        if not self.time: return

        num_columns  = int(self.beatmap.difficulty.cs)
        space_data   = widget.width(), widget.height(), num_columns, self.time
        spatial_data = ManiaSettings.get_spatial_data(*space_data)

        start_time, end_time = spatial_data[0], spatial_data[1]

        for column in range(num_columns):
            start_idx = find(self.beatmap.hitobjects[column], start_time, selector=lambda hitobject: hitobject.time)
            end_idx   = find(self.beatmap.hitobjects[column], end_time,   selector=lambda hitobject: hitobject.get_end_time())

            visible_hitobjects = self.beatmap.hitobjects[column][start_idx : end_idx + 2]
            for visible_hitobject in visible_hitobjects:
                visible_hitobject.render_hitobject(painter, spatial_data[2:], self.time)