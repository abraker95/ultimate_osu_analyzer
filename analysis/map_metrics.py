from misc.geometry import *
from misc.numpy_utils import NumpyUtils
from analysis.map_data import full_hitobject_data


class MapMetrics():


    '''
    Raw metrics
    '''
    @staticmethod
    def calc_tapping_intervals(hitobject_data=full_hitobject_data):
        start_times = hitobject_data.start_times()

        if len(start_times) < 2: return [], []
        intervals = start_times[1:] - start_times[:-1]
    
        return start_times[1:], intervals

    
    @staticmethod
    def calc_velocity(hitobject_data=full_hitobject_data):
        all_times     = hitobject_data.all_times()
        all_positions = hitobject_data.all_positions()

        if len(all_positions) < 2: return [], []
        intervals = NumpyUtils.deltas(all_times)
        
        vel = NumpyUtils.dists(all_positions[1:], all_positions[:-1])/intervals
        return all_times[1:], vel



    @staticmethod
    def calc_angles(hitobject_data=full_hitobject_data):
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
    Advanced metrics
    '''
    @staticmethod
    def calc_rhythmic_complexity(hitobjects):
        pass


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