

class MapMetrics():


    '''
    Raw metrics
    '''
    @staticmethod
    def calc_tapping_intervals(time_list):
        intervals = [ time_list[i] - time_list[i - 1] for i in range(1, len(time_list)) ]
        time      = [ time_list[i] for i in range(1, len(time_list)) ]

        return time, intervals


    @staticmethod
    def calc_velocity(time_pos_list):
        time, pos = zip(*time_pos_list)

        vel  = [ pos[i].distance_to(pos[i - 1])/(time[i] - time[i - 1]) for i in range(1, len(time_pos_list))  ]
        time = [ time[i] for i in range(1, len(time_pos_list)) ]

        return time, vel


    @staticmethod
    def calc_acceleration(hitobjects):
        pass


    @staticmethod
    def calc_angles(hitobjects):
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