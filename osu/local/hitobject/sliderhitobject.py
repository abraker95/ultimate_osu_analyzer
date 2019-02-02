from .hitobject import Hitobject
from ..pos import Pos


class SliderHitobject(Hitobject):

    def __init__(self, beatmap_data):
        Hitobject.__init__(self, beatmap_data)

        self.curve_points = []
        self.__process_slider_data(beatmap_data)
        

    def get_slider_pos(self, time):
        pass


    def get_end_time(self):
        pass


    def get_last_time(self):
        pass


    def get_velocity(self):
        pass


    def __process_slider_data(self, beatmap_data):
        slider_data = beatmap_data[5].split('|')
        self.curve_type = slider_data[0].strip()

        for data in slider_data[1:]:
            curve_data = data.split(':')
            self.curve_points.append(Pos(int(curve_data[0]), int(curve_data[1])))

        if self.is_hitobject_type(Hitobject.SPINNER):
            self.end_time = int(beatmap_data[5])
            return

        if self.is_hitobject_type(Hitobject.MANIALONG):
            slider_data = beatmap_data[5].split(':')
            self.end_time = int(slider_data[0])
            return

        # otherwise this is a osu!std slider and we should get additional data
        self.repeat       = int(beatmap_data[6])
        self.pixel_length = float(beatmap_data[7])