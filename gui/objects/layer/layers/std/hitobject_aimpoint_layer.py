from generic.temporal import Temporal
from gui.objects.layer.layer import Layer

from osu.local.hitobject.std.std import Std


class HitobjectAimpointLayer(Layer, Temporal):

    def __init__(self, data, time_updater):
        Layer.__init__(self, 'Hitobject aimpoints')
        Temporal.__init__(self)

        self.beatmap = data
        
        time_updater.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def paint(self, painter, option, widget):
        if not self.time: return

        ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT

        visible_hitobjects = Std.get_hitobjects_visible_at_time(self.beatmap, self.time)
        for visible_hitobject in visible_hitobjects:
            try: visible_hitobject.render_hitobject_aimpoints(painter, ratio_x, ratio_y)
            except AttributeError: pass