import math



class Mania():

    PLAYFIELD_WIDTH  = 512  # osu!px
    PLAYFIELD_HEIGHT = 384  # osu!px

    @staticmethod
    def is_hitobject_type(hitobject_type, compare):
        return hitobject_type & compare > 0


    @staticmethod
    def get_time_range(hitobjects, column=None):
        if column != None:
            try:    return (hitobjects[column][0].time, hitobjects[column][-1].end_time)
            except: return (hitobjects[column][0].time, hitobjects[column][-1].time)

        all_time_range = [ math.inf, -math.inf ]
        for column in range(len(hitobjects)):
            column_time_range = Mania.get_time_range(hitobjects, column)
            
            all_time_range[0] = min(all_time_range[0], column_time_range[0])
            all_time_range[1] = max(all_time_range[1], column_time_range[1])

        print(all_time_range)
        return (all_time_range[0], all_time_range[1])


    # Returns the key column based on the xpos of the note and the number of keys there are
    @staticmethod
    def get_column(x_pos, columns):
        localWDivisor = Mania.PLAYFIELD_WIDTH / columns
        return min(math.floor(x_pos / localWDivisor), columns - 1)


    