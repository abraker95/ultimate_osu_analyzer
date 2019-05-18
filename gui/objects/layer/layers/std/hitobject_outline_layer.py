from generic.temporal import Temporal
from gui.objects.layer.layer import Layer

from osu.local.hitobject.std.std import Std


class HitobjectOutlineLayer(Layer, Temporal):

    def __init__(self, data, time_driver):
        Layer.__init__(self, 'Hitobject outlines')
        Temporal.__init__(self)

        self.beatmap = data

        time_driver.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def paint(self, painter, option, widget):
        if not self.time: return

        ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT

        visible_hitobjects = Std.get_hitobjects_visible_at_time(self.beatmap, self.time)
        for visible_hitobject in visible_hitobjects:
            try: visible_hitobject.render_hitobject_outline(painter, ratio_x, ratio_y, self.time)
            except AttributeError: pass