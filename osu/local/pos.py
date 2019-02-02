import math


class Pos():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    
    def distance_to(self, pos):
        return math.sqrt(self.x*self.x + self.y*self.y)


    def rot(self, point, radians):
        # TODO
        pass


    def flip(self, axis_radians):
        # TODO
        pass