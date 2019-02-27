import math

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.pos import Pos
from misc.bezier import Bezier
from misc.math_utils import triangle, lerp, value_to_percent
from osu.local.hitobject.hitobject import Hitobject
from osu.local.beatmap.beatmap_utility import BeatmapUtil



"""
Visualizes the osu!std slider

Input: 
    beatmap_data - osu!std slider data read from the beatmap file; determines the type of slider, pos, etc
    time - The time value of the playfield; determine's slider's opacity, follow point position, etc

Output: 
    Visual display of an osu!std slider
"""
class SliderHitobject(QGraphicsItem, Hitobject):

    LINEAR1       = 'L'
    LINEAR2       = 'C'
    BEZIER        = 'B'
    CIRCUMSCRIBED = 'P'

    def __init__(self, beatmap_data):
        QGraphicsItem.__init__(self)
        Hitobject.__init__(self, beatmap_data)

        self.__process_slider_data(beatmap_data)
        self.__process_curve_points()
        

    def time_to_percent(self, time):
        return value_to_percent(self.time, self.end_time, time)


    def time_to_pos(self, time):
        return self.percent_to_pos(self.time_to_percent(time))


    def percent_to_idx(self, percent):
        if percent <= 0.0: return 0
        if percent >= 1.0: return -1 if self.repeat == 0 else 0

        idx = percent*len(self.gen_points)
        idx_pos = triangle(idx*self.repeat, (2 * len(self.gen_points)) - 1)
        
        return int(idx_pos)


    def idx_to_pos(self, idx):
        if idx > len(self.gen_points) - 2:
            return Pos(self.gen_points[-1].x, self.gen_points[-1].y)

        percent_point = float(int(idx)) - idx
        x_pos = lerp(self.gen_points[idx].x, self.gen_points[idx + 1].x, percent_point)
        y_pos = lerp(self.gen_points[idx].y, self.gen_points[idx + 1].y, percent_point)

        return Pos(x_pos, y_pos)


    def percent_to_pos(self, percent):
        return self.idx_to_pos(self.percent_to_idx(percent))


    def get_end_time(self):
        return self.end_time


    def get_last_tick_time(self):
        pass


    def update_slider_tick_pos(self, time):
        self.slider_point_pos = self.time_to_pos(time)


    def paint(self, painter, option, widget):
        painter.setPen(QColor(0, 0, 255, self.opacity*255))

        pos_x = (self.pos.x - self.radius)*self.ratio_x
        pos_y = (self.pos.y - self.radius)*self.ratio_y
        painter.drawEllipse(pos_x, pos_y, 2*self.radius*self.ratio_x, 2*self.radius*self.ratio_y)

        try:
            for i in range(len(self.gen_points) - 1):
                painter.drawLine(self.gen_points[i].x*self.ratio_x, self.gen_points[i].y*self.ratio_y, self.gen_points[i + 1].x*self.ratio_x, self.gen_points[i + 1].y*self.ratio_y)
        except:
            print('Error drawing slider: ', self.gen_points)


        slider_point_radius = 3
        pos_x = (self.slider_point_pos.x - 0.5*slider_point_radius)*self.ratio_x
        pos_y = (self.slider_point_pos.y - 0.5*slider_point_radius)*self.ratio_y
        painter.drawEllipse(pos_x, pos_y, slider_point_radius, slider_point_radius)


    # TODO: make sure this is correct
    # TODO: test a slider 200px across with various repeat times and tick spacings
    def get_velocity(self):
        return self.pixel_length / (self.end_time - self.time)


    def __process_slider_data(self, beatmap_data):
        slider_data = beatmap_data[5].split('|')
        self.curve_type = slider_data[0].strip()

        # The first actual point is the slider's starting position, followed by all other read points
        self.curve_points = [ self.pos ]

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

    
    def __process_curve_points(self):
        self.gen_points  = []

        if self.is_hitobject_type(Hitobject.MANIALONG):
            return

        if self.is_hitobject_type(Hitobject.SPINNER):
            return

        if self.curve_type == SliderHitobject.BEZIER:
            self.__make_bezier()
            self.slider_point_pos = self.gen_points[0]
            return

        if self.curve_type == SliderHitobject.CIRCUMSCRIBED:
            if len(self.curve_points) == 3:
                if not self.__make_circumscribed():
                    self.__make_bezier()
            else:
                self.__make_bezier()

            self.slider_point_pos = self.gen_points[0]
            return

        if self.curve_type == SliderHitobject.LINEAR1:
            self.__make_linear()
            self.slider_point_pos = self.gen_points[0]
            return

        if self.curve_type == SliderHitobject.LINEAR2:
            self.__make_linear()
            self.slider_point_pos = self.gen_points[0]
            return
        
        self.end_point = self.curve_points[-1] if (self.repeat % 2 == 0) else self.curve_points[-1]


    def __make_linear(self):
        # Lines: generate a new curve for each sequential pair
        # ab  bc  cd  de  ef  fg

        for i in range(len(self.curve_points) - 1):
            bezier = Bezier([ self.curve_points[i], self.curve_points[i + 1] ])
            self.gen_points += bezier.curve_points


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
                point_section = [ ]


    def __make_circumscribed(self):
        # construct the three points
        start = self.curve_points[0]
        mid   = self.curve_points[1]
        end   = self.curve_points[2]

        # find the circle center
        mida = start.midpoint(mid)
        midb = end.midpoint(mid)
        nora = (mid - start).nor()
        norb = (mid - end).nor()

        circle_center = self.intersect(mida, nora, midb, norb)
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
        arc_angle = self.pixel_length / radius                                                       # len = theta * r / theta = len / r
        end_angle = start_angle + arc_angle if end_angle > start_angle else start_angle - arc_angle  #  now use it for our new end angle

        # Calculate points
        step = self.pixel_length / 5  # 5 = CURVE_POINTS_SEPERATION
        self.ncurve = step
        len = int(step) + 1

        for i in range(len):
            ang = lerp(start_angle, end_angle, i/step)
            xy  = Pos(math.cos(ang)*radius + circle_center.x, math.sin(ang)*radius + circle_center.y)
            self.gen_points.append(Pos(xy.x, xy.y))
        
        return True

    
    def intersect(self, a, ta, b, tb):
        des = tb.x*ta.y - tb.y*ta.x
        if abs(des) < 0.00001: return None

        u = ((b.y - a.y)*ta.x + (a.x - b.x)*ta.y) / des
        b.x += tb.x*u
        b.y += tb.y*u

        return b


    def boundingRect(self):
        return QRectF(0, 0, self.radius, self.radius)