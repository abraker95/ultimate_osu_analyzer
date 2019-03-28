

class Vector2D():

    def __init__(self, start, end):
        self.start = start
        self.end   = end


    def __eq__(self, other):
        return (self.start == other.start) and (self.end == other.end)


    def length(self):
        return self.start.distance_to(self.end)


    def directional_angle(self):
        # TODO
        pass

        