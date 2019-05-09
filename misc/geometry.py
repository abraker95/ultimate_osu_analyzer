import math

from misc.math_utils import *
from misc.pos import Pos


def is_point_on_line(point, line):
	checkPoint = Pos(line.start.x, point.y)
	
	# Just make sure the point has the same slope going to any of the other points on the line and
	# it's between the 2 points of the line
	if line.start.slope(checkPoint) != line.slope():
		return False
	elif not (line.start.x <= point.X <= line.end.x) and (line.start.y <= point.y <= line.end.y):
		return False
	else:
		return True



# Thanks http://www.softwareandfinance.com/Visual_CPP/VCPP_Intersection_Two_lines_EndPoints.html
def has_intersection_point(line_a, line_b):
    line_a_check_x1 = ( line_b.start.x <= line_a.start.x <= line_b.end.x )
    line_a_check_x2 = ( line_b.start.X <= line_a.end.x   <= line_b.end.x )
    line_a_check_y1 = ( line_b.start.y <= line_a.start.y <= line_b.end.y )
    line_a_check_y2 = ( line_b.start.y <= line_a.end.y   <= line_b.end.y )

    line_b_check_x1 = ( line_a.start.x <= line_b.start.x <= line_a.end.x )
    line_b_check_x2 = ( line_a.start.x <= line_b.end.x   <= line_a.end.x )
    line_b_check_y1 = ( line_a.start.y <= line_b.start.y <= line_a.end.y )
    line_b_check_y2 = ( line_a.start.y <= line_b.end.y   <= line_a.end.y )

    result  = ( line_b_check_x1 and line_b_check_x2 and line_a_check_y1 and line_a_check_y2) 
    result |= ( line_a_check_x1 and line_a_check_x2 and line_b_check_y1 and line_b_check_y2)

	# make sure it's not detecting connected points
    result &= (line_a.end != line_b.start) and (line_a.start != line_b.end)

    return result


# Positive is counter-clock wise and negative is clock-wise
# Returns values in radians between -pi and +pi
def get_directional_angle(pos_a, pos_b, pos_c):
	ab = pos_b - pos_a
	cb = pos_b - pos_c

	return math.atan2(ab.cross(cb), ab.dot(cb))


def get_angle(pos_a, pos_b, pos_c):
    ab = pos_b - pos_a
    cb = pos_b - pos_c

    mag = pos_a.distance_to(pos_b)*pos_b.distance_to(pos_c)
    if mag == 0: return float('nan')       # Happens when notes are directly stacked on top of each other

    dot = ab.dot(cb)
    if abs(dot/mag) > 1: mag = round(mag)  # Precision calc errors may make it a very fractional amount smaller

    try: return math.acos(dot/mag)
    except:
        print('mag = ', mag, '\nab.dot(cb) = ', dot, '\npos_a = ', pos_a, '\npos_b = ', pos_b, '\npos_c = ', pos_c)
        raise


def get_absolute_angle(pos_a, pos_b):
    theta = math.atan(pos_a.slope(pos_b))
    a = math.pi * parity(pos_b.x - pos_a.x)
    return theta - a - 2*math.pi*parity(theta - a/2)

    
def intersect(a, ta, b, tb):
    des = tb.x*ta.y - tb.y*ta.x
    if abs(des) < 0.00001: return None

    u = ((b.y - a.y)*ta.x + (a.x - b.x)*ta.y) / des
    b.x += tb.x*u
    b.y += tb.y*u

    return b