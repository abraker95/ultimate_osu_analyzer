import numpy as np

from misc.geometry import *
from misc.math_utils import *
from misc.metrics import Metrics

from osu.local.beatmap.beatmap import Beatmap

from analysis.osu.std.map_data import StdMapData



class StdMapMetrics():
    """
    Class used for calculating pattern attributes and difficulty.

    .. warning::
        Undocumented functions in this class are not supported and are experimental.
    """

    @staticmethod
    def calc_tapping_intervals(map_data=[]):
        """
        Gets the timing difference between note starting times.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, intervals)``. ``times`` are hitobject timings. ``intervals`` are the timings 
            difference between current and previous note. Resultant array size is ``len(map_data) - 1``.
        """
        t = StdMapData.start_times(map_data)
        dt = np.diff(t)
        return t[1:], dt


    @staticmethod
    def calc_notes_per_sec(map_data=[]):
        """
        Gets number of notes tapped per second based on immidiate duration between notes.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, nps)``. ``times`` are hitobject timings. ``nps`` is notes per second.
            Resultant array size is ``len(map_data) - 1``.
        """
        t = StdMapData.start_times(map_data)
        dt = 1000/np.diff(t)
        return t[1:], dt


    @staticmethod
    def calc_path_dist(map_data=[]):
        """
        Calculates distance between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, dists)``. ``times`` are aimpoint timings. ``dists`` are distances 
            between aimpoints. Resultant array size is ``len(map_data) - 1``.
        """
        t = StdMapData.all_times(map_data)
        x, y = StdMapData.all_positions(map_data)
        return t[1:], Metrics.dists(x, y)

    
    @staticmethod
    def calc_path_vel(map_data=[]):
        """
        Calculates velocity between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, vels)``. ``times`` are aimpoint timings. ``vels`` are based on time and distance
            between aimpoints. Resultant array size is ``len(map_data) - 2``.
        """
        t = StdMapData.all_times(map_data)
        x, y = StdMapData.all_positions(map_data)
        return t[1:], Metrics.vel_2d(x, y, t)


    @staticmethod
    def calc_path_accel(map_data=[]):
        """
        Calculates acceleration between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of (times, accels). ``times`` are aimpoint timings. ``accels`` are based on 
            change in velocity between aimpoints. Resultant array size is ``len(map_data) - 3``.
        """
        t = StdMapData.all_times(map_data)
        x, y = StdMapData.all_positions(map_data)
        return t[1:], Metrics.accel_2d(x, y, t)


    @staticmethod
    def calc_xy_dist(map_data=[]):
        """
        Calculates parametric distance between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks.

        Parameters
        map_data
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, x_dists, y_dists)``. ``times`` are aimpoint timings. ``x_dists`` are distances
            between aimpoints in the x-coordinate direction. ``y_dists`` are distances between aimpoints 
            in the y-coordinate direction. Resultant array size is ``len(map_data) - 1``.
        """
        t = StdMapData.all_times(map_data)
        x, y = StdMapData.all_positions(map_data)
        
        dx = np.diff(x)
        dy = np.diff(y)

        return t[1:], dx, dy


    @staticmethod
    def calc_xy_vel(map_data=[]):
        """
        Calculates parametric velocity between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, x_vels, y_vels)``. ``times`` are aimpoint timings. ``x_vels`` are velocities
            between aimpoints in the x-coordinate direction. ``y_vels`` are velocities between aimpoints 
            in the y-coordinate direction. Resultant array size is ``len(map_data) - 2``.
        """
        t = StdMapData.all_times(map_data)
        x, y = StdMapData.all_positions(map_data)
        
        dt = np.diff(t)
        dx = np.diff(x)
        dy = np.diff(y)

        return t[1:], dx/dt, dy/dt


    @staticmethod
    def calc_xy_accel(map_data=[]):
        """
        Calculates parametric acceleration between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, x_accels, y_accels)``. ``times`` are aimpoint timings. ``x_accels`` are 
            accelerations between aimpoints in the x-coordinate direction. ``y_accels`` are accelerations 
            between aimpoints in the y-coordinate direction. Resultant array size is ``len(map_data) - 3``.
        """
        t, vx, vy = StdMapMetrics.calc_xy_vel(map_data.iloc[2:])

        dvx = np.diff(vx)
        dvy = np.diff(vy)
        dt  = np.diff(t)
        
        return t[1:], dvx/dt, dvy/dt


    @staticmethod
    def calc_xy_jerk(map_data=[]):
        """
        Calculates parametric jerks between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, x_jerks, y_jerks)``. ``times`` are aimpoint timings. ``x_jerks`` are 
            jerks between aimpoints in the x-coordinate direction. ``y_jerks`` are jerks 
            between aimpoints in the y-coordinate direction. Resultant array size is ``len(map_data) - 4``.
        """
        map_data = np.asarray(map_data[2:])
        t, ax, ay = StdMapMetrics.calc_xy_accel(map_data)
        
        dax = np.diff(ax)
        day = np.diff(ay)
        dt  = np.diff(t)
        
        return t[1:], dax/dt, day/dt

    
    @staticmethod
    def calc_velocity_start(map_data=[]):
        t = StdMapData.start_times(map_data)
        x, y = StdMapData.start_positions(map_data)
        return t[1:], Metrics.vel_2d(x, y, t)


    @staticmethod
    def calc_intensity(map_data=[]):
        t, v   = StdMapMetrics.calc_velocity_start(map_data)
        t, nps = StdMapMetrics.calc_notes_per_sec(map_data)

        intensity = v*nps
        return t, intensity


    @staticmethod
    def calc_angles(map_data=[]):
        """
        Calculates angle between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, angles)``. ``times`` are aimpoint timings. ``angles`` are 
            angles between aimpoints. Resultant array size is ``len(map_data) - 1``.
        """
        t = StdMapData.all_times(map_data)
        x, y = StdMapData.all_positions(map_data)
        return t[1:], Metrics.angle(x, y, t)

    
    @staticmethod
    def calc_theta_per_second(map_data=[]):
        """
        Calculates immediate path rotation (in radians per second) from previous aimpoint.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, rps)``. ``times`` are aimpoint timings. ``rps`` are 
            radians per second between aimpoints. Resultant array size is ``len(map_data) - 1``.
        """
        t, thetas = StdMapMetrics.calc_angles(map_data)
        dt = np.diff(t)
        return t[1:], thetas*(1000/dt)


    @staticmethod
    def calc_radial_velocity(map_data=[]):
        """
        Calculates radial velocity between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks. Radial velocity is how fast a path
        moves in a circle in radians per second. Unlike ``calc_theta_per_second``, which 
        calculates immediate rotation, this calculates average rotation.
        
        The difference between the two implemtations is apparent when considering zig-zag and circular patterns.
        Zig-zag patterns has no average angular velocity, but have average linear velocity. In a zig-zag
        pattern one angle would be positive indicating a rotation in a clockwise direction, and another angle 
        would be negative indicating a rotation in a counter-clockwise direction. Ultimately those two cancel 
        out to result in no overall rotation direction. A circular pattern would have either both angles positive 
        or both angles negative, yielding a net negative or a net positive rotation direction.

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, avg_rad_vels)``. ``times`` are aimpoint timings. ``avg_rad_vels`` are 
            average radial velocities. Resultant array size is ``len(map_data) - 2``.
        """
        t = StdMapData.all_times(map_data)
        x, y = StdMapData.all_positions(map_data)
        return t[2:], Metrics.avg_ang_vel(x, y, t[1:])


    @staticmethod
    def calc_perp_int(map_data=[]):
        """
        Calculates perpendicular intensity between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks. Perpendicular intensity is how much strongly the path
        between aimpoints turns 90 deg, factoring in average radial velocity of the path as well as
        overall velocity throughout the path (measured in osu!px*radians/millisconds^2).

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, perp_ints)``. ``times`` are aimpoint timings. ``perp_ints`` are 
            perpendicular intensities. Resultant array size is ``len(map_data) - 2``.
        """
        times, rv = StdMapMetrics.calc_radial_velocity(map_data)
        times, x_vel, y_vel = StdMapMetrics.calc_xy_vel(map_data)

        # Construct vector angles from parametric velocities
        theta1 = np.arctan2(y_vel[1:], x_vel[1:])
        theta2 = np.arctan2(y_vel[:-1], x_vel[:-1])

        # Make stacks 0 angle change
        mask = np.where(np.logical_and(y_vel[1:] == 0, x_vel[1:] == 0))[0]
        theta1[mask] = theta1[mask - 1]

        mask = np.where(np.logical_and(y_vel[:-1] == 0, x_vel[:-1] == 0))[0]
        theta2[mask] = theta2[mask - 1]

        # Velocity in the perpendicular direction relative to current
        dy_vel = np.sin(theta2 - theta1)

        return times, rv*dy_vel[1:]


    # Linear intensity
    @staticmethod
    def calc_lin_int(map_data=[]):
        """
        Calculates linear intensity between aimpoints. Aimpoints are hitobject start 
        and end times, and slider ticks. Linear intensity is how much strongly the path
        between aimpoints is linear, factoring in average radial velocity of the path as well as
        overall velocity throughout the path (measured in osu!px*radians/millisconds^2).

        Parameters
        ----------
        map_data : numpy.array
            Hitobject data from ``StdMapData.get_aimpoint_data``

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(times, lin_ints)``. ``times`` are aimpoint timings. ``lin_ints`` are 
            linear intensities. Resultant array size is ``len(map_data) - 2``.
        """
        times, rv = StdMapMetrics.calc_radial_velocity(map_data)
        times, x_vel, y_vel = StdMapMetrics.calc_xy_vel(map_data)

        # Construct vector angles from parametric velocities
        theta1 = np.arctan2(y_vel[1:], x_vel[1:])
        theta2 = np.arctan2(y_vel[:-1], x_vel[:-1])

        # Make stacks 0 angle change
        mask = np.where(np.logical_and(y_vel[1:] == 0, x_vel[1:] == 0))[0]
        theta1[mask] = theta1[mask - 1]

        mask = np.where(np.logical_and(y_vel[:-1] == 0, x_vel[:-1] == 0))[0]
        theta2[mask] = theta2[mask - 1]

        # Velocity in the parellel direction relative to current
        dx_vel = np.cos(theta2 - theta1)

        return times, rv*dx_vel[1:]
        all_times     = StdMapData.all_times(map_data)
        all_positions = StdMapData.all_positions(map_data)
        if len(all_positions) < 3: return [], []
        
        positions = [ Pos(*pos) for pos in all_positions ]
        angles    = [ get_angle(*param) for param in zip(positions[:-2], positions[1:-1], positions[2:]) ]

        return all_times[1:-1], angles


    @staticmethod
    def calc_acceleration(map_data=[]):
        pass
        pass
        

    '''
    Response metrics
    '''
    @staticmethod
    def calc_speed_response(resolution=1, x_range=(1, 100)):
        return ([x for x in range(*x_range)], [ 1/x for x in range(*x_range) ])


    '''
    Advanced metrics
    '''
    @staticmethod
    def calc_rhythmic_complexity(map_data=[]):
        def calc_harmonic(prev_note_interval, curr_note_interval, target_time, v_scale):
            if prev_note_interval == 0: print('WARNING: 0 note interval detected at ', target_time, ' ms')

            return -(v_scale/2)*math.cos((2*math.pi)/prev_note_interval*curr_note_interval) + (v_scale/2)

        def decay(interval, decay_factor):
            return math.exp(-decay_factor*interval)

        def speed(interval, speed_factor):
            return speed_factor/interval

        def calc_note(time, curr_interval, prev_interval, decay_factor, v_scale):
            return decay(curr_interval, decay_factor) * calc_harmonic(prev_interval, curr_interval, time, v_scale)

        speed_factor = 600.0
        v_factor     = 10.0
        decay_factor = 0.005

        time, intervals = StdMapMetrics.calc_tapping_intervals(map_data)
        harmonics = [ calc_note(time[i], intervals[i], intervals[i - 1], decay_factor, v_factor) for i in range(1, len(intervals)) ]

        return time, [ sum(harmonics[:i])*speed(intervals[i], speed_factor) for i in range(0, len(intervals)) ]


    @staticmethod
    def calc_path_curvature(hitobjects):
        pass
    

    @staticmethod
    def calc_visual_density(hitobjects):
        pass


    '''
    Skill metrics
    '''
    @staticmethod
    def calc_speed_skill(hitobjects):
        pass

    @staticmethod
    def calc_tapping_skill(hitobjects):
        pass


    @staticmethod
    def calc_targeting_skill(hitobjects):
        pass


    @staticmethod
    def calc_agility_skill(hitobjects):
        pass