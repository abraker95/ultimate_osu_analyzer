from .math_utils import bernstein
from .pos import Pos


class Bezier():

    def __init__(self, curve_points):
        self.curve_points    = []
        self.curve_distances = [ 0 ]
        self.total_distance  = 0

        # Estimate the length of the curve
        approx_length = 0
        for i in range(len(curve_points) - 1):
            approx_length += curve_points[i].distance_to(curve_points[i + 1])

        # subdivide the curve
        ncurve = int(approx_length / 4.0) + 2
        for i in range(ncurve):
            self.curve_points.append(Bezier.point_at(curve_points, float(i) / float(ncurve - 1)))

        # find the distance of each point from the previous point
        for i in range(1, len(curve_points)):
            self.curve_distances.append(curve_points[i].distance_to(curve_points[i - 1]))
            self.total_distance += self.curve_distances[i]


    # Returns the points along the curve of the Bezier curve.
    def get_curve_points(self):
        return self.curve_points


    # Returns the distances between a point of the curve and the last point.
    def get_curve_distances(self):
        return self.curve_distances


    #  Returns the total distances of this Bezier curve.
    def get_total_curve_distance(self):
        return self.total_distance
    

    @staticmethod
    def point_at(curve_points, t):
        c = Pos(0, 0)
        n = len(curve_points)

        for i in range(n):
            b = bernstein(i, n - 1, t)
            c += Pos(curve_points[i].x * b, curve_points[i].y * b)

        return c