from ..pos import Pos



class Hitobject():

    CIRCLE  = 1 << 0
    SLIDER  = 1 << 1
    NCOMBO  = 1 << 2
    SPINNER = 1 << 3
    # ???
    MANIALONG = 1 << 7

    def __init__(self, beatmap_data=None):
        if beatmap_data is None:
            self.hitobject_type = None
            self.time  = None
            self.index = None
            self.pos   = None
            self.type  = None

        if beatmap_data:
            self.__process_hitobject_data(beatmap_data)


    def get_copy(self):
        pass


    def is_hitobject_type(self, hitobject_type):
        return self.hitobject_type & hitobject_type > 0


    def is_hitobject_long(self):
        pass


    def __process_hitobject_data(self, data):
        self.pos            = Pos(int(data[0]), int(data[1]))
        self.time           = int(data[2])
        self.hitobject_type = int(data[3])