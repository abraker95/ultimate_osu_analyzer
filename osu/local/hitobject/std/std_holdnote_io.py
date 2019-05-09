import math

from misc.pos import Pos
from misc.bezier import Bezier
from misc.math_utils import triangle, lerp, value_to_percent
from misc.geometry import intersect
from osu.local.hitobject.std.std_holdnote_hitobject import StdHoldNoteHitobject


class StdHoldNoteIO():

    @staticmethod
    def load_holdnote(data):
        holdnote = StdHoldNoteHitobject()
        if not data: return holdnote

        StdHoldNoteIO.__process_hitobject_data(data, holdnote)
        StdHoldNoteIO.__process_slider_data(data, holdnote)
        StdHoldNoteIO.__process_curve_points(holdnote)

        return holdnote


    @staticmethod
    def get_data(self, holdnote):
        # TODO
        pass


    @staticmethod
    def __process_hitobject_data(data, holdnote):
        holdnote.pos            = Pos(int(data[0]), int(data[1]))
        holdnote.time           = int(data[2])
        holdnote.hitobject_type = int(data[3])


    @staticmethod
    def __process_slider_data(data, holdnote):
        slider_data = data[5].split('|')
        holdnote.curve_type = slider_data[0].strip()

        # The first actual point is the slider's starting position, followed by all other read points
        holdnote.curve_points = [ holdnote.pos ]

        for curve_data in slider_data[1:]:
            curve_data = curve_data.split(':')
            holdnote.curve_points.append(Pos(int(curve_data[0]), int(curve_data[1])))

        # otherwise this is a osu!std slider and we should get additional data
        holdnote.repeat       = int(data[6])
        holdnote.pixel_length = float(data[7])

    
    @staticmethod
    def __process_curve_points(holdnote):
        holdnote.gen_points  = []

        if holdnote.curve_type == StdHoldNoteHitobject.BEZIER:
            StdHoldNoteIO.__make_bezier(holdnote)
            holdnote.slider_point_pos = holdnote.gen_points[0]
            return

        if holdnote.curve_type == StdHoldNoteHitobject.CIRCUMSCRIBED:
            if len(holdnote.curve_points) == 3:
                if not StdHoldNoteIO.__make_circumscribed(holdnote):
                    StdHoldNoteIO.__make_bezier(holdnote)
            else:
                StdHoldNoteIO.__make_bezier(holdnote)

            holdnote.slider_point_pos = holdnote.gen_points[0]
            return

        if holdnote.curve_type == StdHoldNoteHitobject.LINEAR1:
            StdHoldNoteIO.__make_linear(holdnote)
            holdnote.slider_point_pos = holdnote.gen_points[0]
            return

        if holdnote.curve_type == StdHoldNoteHitobject.LINEAR2:
            StdHoldNoteIO.__make_linear(holdnote)
            holdnote.slider_point_pos = holdnote.gen_points[0]
            return
        
        holdnote.end_point = holdnote.curve_points[-1] if (holdnote.repeat % 2 == 0) else holdnote.curve_points[-1]


    @staticmethod
    def __make_linear(self):
        # Lines: generate a new curve for each sequential pair
        # ab  bc  cd  de  ef  fg

        for i in range(len(self.curve_points) - 1):
            bezier = Bezier([ self.curve_points[i], self.curve_points[i + 1] ])
            self.gen_points += bezier.curve_points


    @staticmethod
    def __make_bezier(self):
        # Beziers: splits points into different Beziers if has the same points (red points)
        # a b c - c d - d e f g
        point_section = []

        for i in range(len(self.curve_points)):
            point_section.append(self.curve_points[i])

            not_end_of_list = (i < len(self.curve_points) - 1)
            segment_bezier  = (self.curve_points[i] == self.curve_points[i + 1]) if not_end_of_list else True

            # If we reached a red point or the end of the point list, then segment the bezier
            if segment_bezier:
                self.gen_points += Bezier(point_section).curve_points
                point_section = []


    @staticmethod
    def __make_circumscribed(holdnote):
        # construct the three points
        start = holdnote.curve_points[0]
        mid   = holdnote.curve_points[1]
        end   = holdnote.curve_points[2]

        # find the circle center
        mida = start.midpoint(mid)
        midb = end.midpoint(mid)
        nora = (mid - start).nor()
        norb = (mid - end).nor()

        circle_center = intersect(mida, nora, midb, norb)
        if not circle_center: return False

        start_angle_point = start - circle_center
        mid_angle_point   = mid - circle_center
        end_angle_point   = end - circle_center

        start_angle = math.atan2(start_angle_point.y, start_angle_point.x)
        mid_angle   = math.atan2(mid_angle_point.y, mid_angle_point.x)
        end_angle   = math.atan2(end_angle_point.y, end_angle_point.x)

        if not start_angle < mid_angle < end_angle:
            if abs(start_angle + 2*math.pi - end_angle) < 2*math.pi and (start_angle + 2*math.pi < mid_angle < end_angle):
                start_angle += 2*math.pi
            elif abs(start_angle - (end_angle + 2*math.pi)) < 2*math.pi and (start_angle < mid_angle < end_angle + 2*math.pi):
                end_angle += 2*math.pi
            elif abs(start_angle - 2*math.pi - end_angle) < 2*math.pi and (start_angle - 2*math.pi < mid_angle < end_angle):
                start_angle -= 2*math.pi
            elif abs(start_angle - (end_angle - 2*math.pi)) < 2*math.pi and (start_angle < mid_angle < end_angle - 2*math.pi):
                end_angle -= 2*math.pi   
            else:
                print('Cannot find angles between mid_angle')
                return False

        # find an angle with an arc length of pixelLength along this circle
        radius = start_angle_point.distance_to(Pos(0, 0))
        arc_angle = holdnote.pixel_length / radius                                                       # len = theta * r / theta = len / r
        end_angle = start_angle + arc_angle if end_angle > start_angle else start_angle - arc_angle  #  now use it for our new end angle

        # Calculate points
        step = holdnote.pixel_length / 5  # 5 = CURVE_POINTS_SEPERATION
        holdnote.ncurve = step
        len = int(step) + 1

        for i in range(len):
            ang = lerp(start_angle, end_angle, i/step)
            xy  = Pos(math.cos(ang)*radius + circle_center.x, math.sin(ang)*radius + circle_center.y)
            holdnote.gen_points.append(Pos(xy.x, xy.y))
        
        return True