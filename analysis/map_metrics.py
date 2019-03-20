

class MapMetrics():

    @staticmethod
    def hitobject_start_times(hitobjects):
        return [ hitobjects[i].time for i in range(1, len(hitobjects)) ]

    '''
    Raw metrics
    '''
    @staticmethod
    def calc_tapping_intervals(hitobjects):
        return [ hitobjects[i].time - hitobjects[i - 1].time for i in range(1, len(hitobjects)) ]


    @staticmethod
    def calc_velocity(hitobjects):
        pass


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