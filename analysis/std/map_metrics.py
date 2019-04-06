from misc.geometry import *
from misc.numpy_utils import NumpyUtils
from analysis.std.map_data import MapData


class MapMetrics():


    '''
    Raw metrics
    '''
    @staticmethod
    def calc_tapping_intervals(hitobject_data=MapData.full_hitobject_data):
        start_times = hitobject_data.start_times()

        if len(start_times) < 2: return [], []
        intervals = start_times[1:] - start_times[:-1]
    
        return start_times[1:], intervals

    
    @staticmethod
    def calc_velocity(hitobject_data=MapData.full_hitobject_data):
        all_times     = hitobject_data.all_times()
        all_positions = hitobject_data.all_positions()

        if len(all_positions) < 2: return [], []
        intervals = NumpyUtils.deltas(all_times)
        
        vel = NumpyUtils.dists(all_positions[1:], all_positions[:-1])/intervals
        return all_times[1:], vel



    @staticmethod
    def calc_angles(hitobject_data=MapData.full_hitobject_data):
        all_times     = hitobject_data.all_times()
        all_positions = hitobject_data.all_positions()
        if len(all_positions) < 3: return [], []
        
        positions = [ Pos(*pos) for pos in all_positions ]
        angles    = [ get_angle(*param) for param in zip(positions[:-2], positions[1:-1], positions[2:]) ]

        return all_times[1:-1], angles


    @staticmethod
    def calc_acceleration(hitobjects):
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
    def calc_rhythmic_complexity(hitobject_data=MapData.full_hitobject_data):
        def calc_harmonic(prev_note_interval, curr_note_interval, target_time, v_scale):
            if prev_note_interval == 0: print('WARNING: 0 note interval detected at ', target_time, ' ms')

            return -(v_scale/2)*math.cos((2*math.pi)/prev_note_interval*curr_note_interval) + (v_scale/2)

        def decay(interval, decay_factor):
            return math.exp(-decay_factor*interval)

        def speed(interval, speed_factor):
            return speed_factor/interval

        def calc_note(time, curr_interval, prev_interval, speed_factor, v_scale):
            return decay(curr_interval, speed_factor) * calc_harmonic(prev_interval, curr_interval, time, v_scale)

        speed_factor = 600.0
        v_factor     = 10.0
        speed_factor = 0.005

        time, intervals = MapMetrics.calc_tapping_intervals(hitobject_data)
        harmonics = [ calc_note(time[i], intervals[i], intervals[i - 1], speed_factor, v_factor) for i in range(1, len(intervals)) ]

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