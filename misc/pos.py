import math


"""
Object holds 2D coordinate data and provides 2D geometric operations

Input: 
    x - x-coordinate
    y - y-coordinate
"""
class Pos():

    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __ne__(self, other):
        return not (self == other)


    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)


    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)


    def __mul__(self, other):
        return Pos(self.x * other.x, self.y * other.y)


    def __truediv__(self, other):
        return Pos(self.x / other.x, self.y / other.y)


    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


    def distance_to(self, pos):
        x_delta = self.x - pos.x
        y_delta = self.y - pos.y
        return math.sqrt(x_delta*x_delta + y_delta*y_delta)


    def midpoint(self, other):
        return (other + self)/Pos(2.0, 2.0)


    def slope(self, other):
        if self.x - other.x == 0: return float('inf')
        else:                     return (self.y - other.y) / (self.x - other.x) 


    def nor(self):
        return Pos(-self.y, self.x)


    def rot(self, point, radians):
        # TODO
        pass


    def flip(self, axis_radians):
        # TODO
        pass


    def abs(self):
        return Pos(abs(self.x), abs(self.y))

    
    def dot(self, other):
        return self.x*other.x + self.y*other.y


    def cross(self, other):
        return self.y*other.y - self.y*other.x