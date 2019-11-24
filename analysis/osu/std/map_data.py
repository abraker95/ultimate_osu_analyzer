import numpy as np
import itertools

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.std.std import Std
from misc.numpy_utils import NumpyUtils



class StdMapData():
    """
    Class used for navigating, extracting, and operating on map data.
    
    .. note::
        This is not to be confused with the map data in the Beatmap class.
        Data used by this class is in numpy array form. Data in the Beatmap 
        class is based on *.osu file structure and is not in a friendly 
        format to perform analysis on.
    """

    TIME = 0
    POS  = 1

    @staticmethod 
    def std_hitobject_to_aimpoints(std_hitobject):
        """
        Converts a Hitobject type into a numpy array equivalent that can 
        be used by the analysis framework.

        .. warning::
            This function is not intended to be used directly

        Parameters
        ----------
        std_hitobject : Hitobject
            A hitobject to convert

        Returns
        -------
        generator object
            A list of

                [ start_time, [ (scorepoint_x, scorepoint), ... ] ]

            Hitcircles contain only one scorepoint. Sliders can contain
            more than one. This format is reflected in the groups of 
            [ time, pos ] in the map data
        """
        if std_hitobject.is_hitobject_type(Hitobject.CIRCLE):
            yield [ std_hitobject.time, (std_hitobject.pos.x, std_hitobject.pos.y) ]
        
        elif std_hitobject.is_hitobject_type(Hitobject.SLIDER):
            for aimpoint_time in std_hitobject.get_aimpoint_times():
                yield [ aimpoint_time, np.asarray([ std_hitobject.time_to_pos(aimpoint_time).x, std_hitobject.time_to_pos(aimpoint_time).y ]) ]

    
    @staticmethod
    def std_hitobjects_to_aimpoints(std_hitobjects):
        """
        Converts a list of Hitobject types into a numpy array equivalent that can 
        be used by the analysis framework.

        .. warning::
            This function is not intended to be used directly

        Parameters
        ----------
        std_hitobjects : Hitobject
            List of hitobjects to convert

        Returns
        -------
        generator object
            A complied list of a aimpoints
        """
        for hitobject in std_hitobjects:
            aimpoints = list(StdMapData.std_hitobject_to_aimpoints(hitobject))

            # If last slider aimpoint is within a certain slider circle distance of first aimpoint, then filter out
            if len(aimpoints) > 1:
                aimpoint_ax, aimpoint_ay = aimpoints[0][1][0], aimpoints[0][1][1]
                aimpoint_bx, aimpoint_by = aimpoints[0][-1][0], aimpoints[0][-1][1]
                
                dist = math.sqrt((aimpoint_bx - aimpoint_ax)**2 - (aimpoint_by - aimpoint_ay)**2)
                if dist < 50: aimpoints = aimpoints[:-1]

            if len(aimpoints) > 0: yield aimpoints


    @staticmethod
    def get_aimpoint_data(std_hitobjects):
        """
        Converts a list of Hitobject types into a numpy array equivalent that can 
        be used by the analysis framework.

        .. note::
            This function is intended to be used directly

        Parameters
        ----------
        std_hitobjects : Hitobject
            List of hitobjects to convert

        Returns
        -------
        A numpy array with the following format representing map data:

            [
                [ 
                    [ time, pos ],
                    [ time, pos ],
                    ... N score points
                ],
                [ 
                    [ time, pos ],
                    [ time, pos ],
                    ...  N score points
                ],
                ... N hitobjects
            ]

        """
        return np.asarray(list(StdMapData.std_hitobjects_to_aimpoints(std_hitobjects)))


    @staticmethod
    def get_data_before(map_data, time):
        """
        Get the closest scorepoint right before the desired point in time

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on
        
        time : int
            Desired point in time

        Returns
        -------
        Scorepoint data

            [ time, (scorepoint_x, scorepoint_y) ]

        """
        idx_time = StdMapData.get_idx_start_time(map_data, time)

        if not idx_time: return None
        if idx_time < 1: return None

        return map_data[idx_time - 1][-1]


    @staticmethod
    def get_data_after(map_data, time):
        """
        Get all scorepoints before the desired point in time

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on
        
        time : int
            Desired point in time

        Returns
        -------
        Scorepoint data

            [ time, (scorepoint_x, scorepoint_y) ]
            
        """
        idx_time = StdMapData.get_idx_end_time(map_data, time)
        
        if not idx_time:                       return None
        if idx_time > len(map_data) - 2: return None
            
        return map_data[idx_time + 1][0]


    @staticmethod
    def time_slice(map_data, start_time, end_time):
        start_idx = StdMapData.get_idx_start_time(map_data, start_time)
        end_idx   = StdMapData.get_idx_end_time(map_data, end_time)

        return map_data[start_idx:end_idx]


    @staticmethod
    def start_times(map_data):
        return np.asarray([ note[0][StdMapData.TIME] for note in map_data ])


    @staticmethod
    def end_times(map_data):
        return np.asarray([ note[-1][StdMapData.TIME] for note in map_data ])


    @staticmethod
    def start_positions(map_data):
        return np.asarray([ note[0][StdMapData.POS] for note in map_data ])

    
    @staticmethod
    def end_positions(map_data):
        return np.asarray([ note[-1][StdMapData.POS] for note in map_data ])


    @staticmethod
    def all_positions(map_data, flat=True):
        if flat: return np.asarray([ data[StdMapData.POS] for note in map_data for data in note ])
        else:    return np.asarray([[data[StdMapData.POS] for data in note] for note in map_data])


    @staticmethod
    def all_times(map_data, flat=True):
        if flat: return np.asarray([ data[StdMapData.TIME] for note in map_data for data in note ])
        else:    return np.asarray([[data[StdMapData.TIME] for data in note] for note in map_data])

    
    @staticmethod
    def start_end_times(map_data):
        all_times = StdMapData.all_times(map_data, flat=False)
        return np.asarray([ (hitobject_times[0], hitobject_times[-1]) for hitobject_times in all_times ])


    @staticmethod
    def get_idx_start_time(map_data, time):
        if type(time) == type(None): return None

        times = np.asarray(StdMapData.start_times(map_data))
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))

    
    @staticmethod
    def get_idx_end_time(map_data, time):
        if type(time) == type(None): return None
            
        times = np.asarray(StdMapData.end_times(map_data))
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))








    '''
    def append_to_end(self, raw_data, is_part_of_hitobject=False):
        if raw_data == None:   return
        if len(raw_data) == 0: return
    
        if is_part_of_hitobject: self.hitobject_data[-1].append(raw_data)
        else:                    self.hitobject_data.append([ raw_data ])


    def append_to_start(self, raw_data, is_part_of_hitobject=False):
        if raw_data == None:   return
        if len(raw_data) == 0: return
        
        if is_part_of_hitobject: self.hitobject_data[0].insert(0, raw_data)
        else:                    self.hitobject_data.insert(0, [ raw_data ])
    '''