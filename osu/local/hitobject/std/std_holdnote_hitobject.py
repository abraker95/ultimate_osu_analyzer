import math

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from misc.pos import Pos
from misc.bezier import Bezier
from misc.frozen_cls import FrozenCls
from misc.math_utils import triangle, lerp, value_to_percent

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.std.std import Std



"""
Visualizes the osu!std slider

Input: 
    beatmap_data - osu!std slider data read from the beatmap file; determines the type of slider, pos, etc
    time - The time value of the playfield; determine's slider's opacity, follow point position, etc

Output: 
    Visual display of an osu!std slider
"""
@FrozenCls
class StdHoldNoteHitobject(Hitobject):

    LINEAR1       = 'L'
    LINEAR2       = 'C'
    BEZIER        = 'B'
    CIRCUMSCRIBED = 'P'

    def __init__(self):
        self.end_time     = None    # Initialized by beatmapIO.__process_slider_timings after timing data is read
        self.pixel_length = None
        self.repeat       = None
        self.curve_type   = None

        self.to_repeat_time   = None

        self.curve_points = []  # Points that define slider in editor
        self.gen_points   = []  # The rough generated slider curve
        self.tick_times   = []  # Slider ticks/score points/aimpoints

        Hitobject.__init__(self)
        

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


    def get_generated_curve_points(self):
        return self.gen_points


    def get_last_tick_time(self):
        return self.tick_times[-1]


    def get_aimpoints(self):
        return self.tick_times


    def raw_data(self):
        return [ [ tick_time, (self.time_to_pos(tick_time).x, self.time_to_pos(tick_time).y) ] for tick_time in self.tick_times ]


    # TODO: make sure this is correct
    # TODO: test a slider 200px across with various repeat times and tick spacings
    def get_velocity(self):
        return self.pixel_length / (self.end_time - self.time)


    def time_changed(self, time):
        self.slider_point_pos = self.time_to_pos(time)


    def render_hitobject_outline(self, painter, ratio_x, ratio_y, time):
        painter.setPen(QColor(0, 0, 255, self.opacity*255))

        radius = Std.cs_to_px(self.difficulty.cs)
        pos_x  = (self.pos.x - radius)*ratio_x
        pos_y  = (self.pos.y - radius)*ratio_y
        painter.drawEllipse(pos_x, pos_y, 2*radius*ratio_x, 2*radius*ratio_y)

        try:
            for i in range(len(self.gen_points) - 1):
                painter.drawLine(self.gen_points[i].x*ratio_x, self.gen_points[i].y*ratio_y, self.gen_points[i + 1].x*ratio_x, self.gen_points[i + 1].y*ratio_y)
        except:
            print('Error drawing slider: ', self.gen_points)

        # Let it be part of hitobject outline
        self.render_sliderpoint(painter, ratio_x, ratio_y, time)


    def render_sliderpoint(self, painter, ratio_x, ratio_y, time):
        painter.setPen(QColor(0, 0, 255, self.opacity*255))
        
        slider_point_radius = 3
        slider_point_pos = self.time_to_pos(time)

        pos_x = (slider_point_pos.x - 0.5*slider_point_radius)*ratio_x
        pos_y = (slider_point_pos.y - 0.5*slider_point_radius)*ratio_y
        painter.drawEllipse(pos_x, pos_y, slider_point_radius, slider_point_radius)


    def render_hitobject_aimpoints(self, painter, ratio_x, ratio_y):
        painter.setPen(QColor(255, 0, 255, self.opacity*255))
        slider_tick_radius = 6

        for tick_time in self.tick_times:
            tick_pos = self.time_to_pos(tick_time)

            pos_x = (tick_pos.x - 0.5*slider_tick_radius)*ratio_x
            pos_y = (tick_pos.y - 0.5*slider_tick_radius)*ratio_y
            painter.drawEllipse(pos_x, pos_y, slider_tick_radius, slider_tick_radius)


    def boundingRect(self):
        radius = BeatmapUtil.cs_to_px(self.difficulty.cs)
        return QRectF(0, 0, radius, radius)