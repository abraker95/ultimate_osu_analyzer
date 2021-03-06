import math
from misc.callback import callback


# Drawing parameters
class ManiaSettings():

    viewable_time_interval = 1000   # ms
    note_width             = 50     # osu!px
    note_height            = 15     # osu!px
    note_seperation        = 5      # osu!px
    replay_opacity         = 50     # %

    @staticmethod
    @callback
    def set_viewable_time_interval(viewable_time_interval):
        ManiaSettings.viewable_time_interval = viewable_time_interval
        ManiaSettings.set_viewable_time_interval.emit()


    @staticmethod
    @callback
    def set_note_width(note_width):
        ManiaSettings.note_width = note_width
        ManiaSettings.set_note_width.emit()


    @staticmethod
    @callback
    def set_note_height(note_height):
        ManiaSettings.note_height = note_height
        ManiaSettings.set_note_height.emit()


    @staticmethod
    @callback
    def set_note_seperation(note_seperation):
        ManiaSettings.note_seperation = note_seperation
        ManiaSettings.set_note_seperation.emit()


    @staticmethod
    @callback
    def set_replay_opacity(replay_opacity):
        ManiaSettings.replay_opacity = replay_opacity
        ManiaSettings.set_replay_opacity.emit()


    @staticmethod 
    def get_spatial_data(space_width, space_height, num_columns, time):
        ratio_x = space_width/Mania.PLAYFIELD_WIDTH                  # px per osu!px
        ratio_y = space_height/Mania.PLAYFIELD_HEIGHT                # px per osu!px
        ratio_t = space_height/ManiaSettings.viewable_time_interval  # px per ms

        total_width = num_columns*(ManiaSettings.note_width + ManiaSettings.note_seperation)*ratio_x
        start_time  = time
        end_time    = time + ManiaSettings.viewable_time_interval

        x_offset = space_width/2.0 - total_width/2.0
        y_offset = space_height

        return start_time, end_time, ratio_x, ratio_y, ratio_t, x_offset, y_offset


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


    @staticmethod
    def get_acc_from_hits(num_300_hits, num_200_hits, num_100_hits, num_50_hits, num_misses):
        score_hits  = 50*num_50_hits + 100*num_100_hits + 200*num_200_hits + 300*num_300_hits
        score_total = 300*(num_misses + num_50_hits + num_100_hits + num_200_hits + num_300_hits)
        return score_hits/score_total


    # Returns the key column based on the xpos of the note and the number of keys there are
    @staticmethod
    def get_column(x_pos, columns):
        ratio = columns / Mania.PLAYFIELD_WIDTH   # columns per osu!px
        return min(math.floor(ratio*x_pos), columns - 1)


    @staticmethod
    def get_key_presses(key_val):
        # Generator yielding value of each bit in an integer if it's set + value
        # of LSB no matter what .
        def bits(n):
            if n == 0: yield 0
            while n:
                b = n & (~n+1)
                yield b
                n ^= b

        def keys(bit_list):
            for bit in bit_list:
                if bit == 0: continue
                yield math.log2(bit)

        return keys(bits(int(key_val)))
    