import numpy as np
import math
import itertools

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.std.std import Std
from misc.numpy_utils import NumpyUtils



class StdMapData():
    """
    Class used for navigating, extracting, and operating on standard gamemode map data.
    
    .. note::
        This is not to be confused with the map data in the osu.local.beatmap.beatmap.Beatmap class.
        Data used by this class is in numpy array form. Data in the Beatmap 
        class is based on *.osu file structure and is not in a friendly 
        format to perform analysis on.
    """

    TIME = 0
    POS  = 1

    @staticmethod 
    def std_hitobject_to_aimpoints(std_hitobject):
        """
        .. warning::
            This function is not intended to be used directly

        Converts a ``Hitobject`` type into a numpy array equivalent that can 
        be used by the analysis framework.

        Parameters
        ----------
        std_hitobject : Hitobject
            A hitobject to convert

        Returns
        -------
        generator object
            A list of scorepoints in the following format:
            ::

                [
                    [ start_time, [ (scorepoint_x, scorepoint), ... ] ],
                    [ start_time, [ (scorepoint_x, scorepoint), ... ] ],
                    ...
                ]

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
        .. warning::
            This function is not intended to be used directly

        Converts a list of ``Hitobject`` types into a numpy array equivalent that can 
        be used by the analysis framework.

        Parameters
        ----------
        std_hitobjects : Hitobject
            List of hitobjects to convert

        Returns
        -------
        generator object
            A complied list of aimpoints
        """
        for hitobject in std_hitobjects:
            aimpoints = list(StdMapData.std_hitobject_to_aimpoints(hitobject))

            # If last slider aimpoint is within a certain slider circle distance of first aimpoint, then filter out
            if len(aimpoints) > 1:
                aimpoint_ax, aimpoint_ay = aimpoints[0][1][0], aimpoints[0][1][1]
                aimpoint_bx, aimpoint_by = aimpoints[0][-1][0], aimpoints[0][-1][1]
                
                dist = math.sqrt((aimpoint_bx - aimpoint_ax)**2 - (aimpoint_by - aimpoint_ay)**2)
                #if dist < 50: aimpoints = aimpoints[:-1]

            if len(aimpoints) > 0: yield aimpoints


    @staticmethod
    def get_aimpoint_data(std_hitobjects):
        """
        .. note::
            This function is intended to be used directly

        Converts a list of ``Hitobject`` types into a numpy array equivalent that can 
        be used by the analysis framework.

        Parameters
        ----------
        std_hitobjects : Hitobject
            List of hitobjects to convert

        Returns
        -------
        numpy.array
            Map data representing the following format:
            ::
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
        numpy.array
            Scorepoint data
            ::
                [ time, (scorepoint_x, scorepoint_y) ]

        """
        idx_time = StdMapData.get_idx_start_time(map_data, time)

        if not idx_time: return None
        if idx_time < 1: return None

        return map_data[idx_time - 1][-1]


    @staticmethod
    def get_data_after(map_data, time):
        """
        Get the closest scorepoints right after the desired point in time

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on
        
        time : int
            Desired point in time

        Returns
        -------
        numpy.array
            Scorepoint data
            ::
                [ time, (scorepoint_x, scorepoint_y) ]
            
        """
        idx_time = StdMapData.get_idx_end_time(map_data, time)
        
        if not idx_time:                       return None
        if idx_time > len(map_data) - 2: return None
            
        return map_data[idx_time + 1][0]


    @staticmethod
    def time_slice(map_data, start_time, end_time):
        """
        Gets a list of hitobjects data that occurs between ``start_time`` and ``end_time``

        Parameters
        ----------
        map_data : numpy.array
            Map data to get the slice of data for

        start_time : int
            Starting time for the slice of data
        
        end_time : int
            Ending time for the slice of data

        Returns
        -------
        numpy.array
            Hitobject data
            ::
                array([
                    list([
                        [ time, [scorepoint_x, scorepoint_y] ]
                        [ time, [scorepoint_x, scorepoint_y] ]
                        ...
                    ]),
                    list([
                        [ time, [scorepoint_x, scorepoint_y] ]
                        [ time, [scorepoint_x, scorepoint_y] ]
                        ...
                    ]),
                    ...
                ])
            
        """
        start_idx = StdMapData.get_idx_start_time(map_data, start_time)
        end_idx   = StdMapData.get_idx_end_time(map_data, end_time)

        return map_data[start_idx:end_idx]


    @staticmethod
    def start_times(map_data):
        """
        Gets the start times of all hitobjects

        Parameters
        ----------
        map_data : numpy.array
            Map data to get hitobject start times for

        Returns
        -------
        numpy.array
            Hitobject start times
            ::
                [ time, time, time, ... ]
            
        """
        return np.asarray([ note[0][StdMapData.TIME] for note in map_data ])


    @staticmethod
    def end_times(map_data):
        """
        Get gets the end times of all hitobjects

        .. note::
            Hitcircle hitobjects will have the same start and end times

        Parameters
        ----------
        map_data : numpy.array
            Map data to get hitobject end times for

        Returns
        -------
        numpy.array
            End times of hitobjects
            ::
                [ time, time, time, ... ]
            
        """
        return np.asarray([ note[-1][StdMapData.TIME] for note in map_data ])


    @staticmethod
    def start_positions(map_data):
        """
        Gets the starting positions of all hitobjects

        Parameters
        ----------
        map_data : numpy.array
            Map data to get hitobject starting positions for

        Returns
        -------
        numpy.array
            Hitobject starting positions
            ::
                [ 
                    [ pos_x, pos_y ], 
                    [ pos_x, pos_y ], 
                    ... 
                ]
            
        """
        return np.asarray([ note[0][StdMapData.POS] for note in map_data ])

    
    @staticmethod
    def end_positions(map_data):
        """
        Gets the ending positions of all hitobjects

        .. note::
            Hitcircle hitobjects will have the same start and end positions

        Parameters
        ----------
        map_data : numpy.array
            Map data to get hitobject ending positions for

        Returns
        -------
        numpy.array
            Ending positions of hitobject
            ::
                [ 
                    [ pos_x, pos_y ], 
                    [ pos_x, pos_y ], 
                    ... 
                ]
            
        """
        return np.asarray([ note[-1][StdMapData.POS] for note in map_data ])


    @staticmethod
    def all_positions(map_data, flat=True):
        """
        Gets positions data for all hitobjects in the map

        Parameters
        ----------
        map_data : numpy.array
            Map data to get position data for

        flat : boolean
            Whether to return as flat scorepoint data or preserve
            hitobject information

        Returns
        -------
        numpy.array
            If flat = True, returns numpy array of scorepoint positions
            ::
                [ 
                    [ pos_x, pos_y ], 
                    [ pos_x, pos_y ], 
                    ... 
                ]

            If flat = False, returns numpy array of list of scorepoint positions grouped by hitobject
            ::
                [ 
                    list([
                            [ scorepoint_x, scorepoint_y ],
                            [ scorepoint_x, scorepoint_y ],
                            ...
                    ]),
                    list([
                            [ scorepoint_x, scorepoint_y ],
                            [ scorepoint_x, scorepoint_y ],
                            ...
                    ]),
                    ...,
                    list([ (scorepoint_x, scorepoint_y) ]),
                    list([ (scorepoint_x, scorepoint_y) ]),
                    ...
                ]
            
        """
        if flat: return np.asarray([ data[StdMapData.POS] for note in map_data for data in note ])
        else:    return np.asarray([[data[StdMapData.POS] for data in note] for note in map_data])


    @staticmethod
    def all_times(map_data, flat=True):
        """
        Gets time data for all hitobjects in the map

        Parameters
        ----------
        map_data : numpy.array
            Map data to get position data for

        flat : boolean
            Whether to return as flat scorepoint data or preserve
            hitobject information

        Returns
        -------
        numpy.array
            If flat = True, returns numpy array of scorepoint times
            ::
                [ time, time, time, ... ]

            If flat = False, returns numpy array of list of scorepoint times grouped by hitobject
            ::
                [ 
                    list([ time, time, ... ]),
                    list([ time, time, ... ]),
                    ...,
                    list([ time ]),
                    list([ time ]),
                    ...
                ]
            
        """
        if flat: return np.asarray([ data[StdMapData.TIME] for note in map_data for data in note ])
        else:    return np.asarray([[data[StdMapData.TIME] for data in note] for note in map_data])

    
    @staticmethod
    def start_end_times(map_data):
        """
        Gets pairs of start and ending times for all hitobjects in the map

        Parameters
        ----------
        map_data : numpy.array
            Map data to get start and end times of hitobjects for

        Returns
        -------
        numpy.array
            Pairs of start and end times
            ::
                [ 
                    [ start_time, end_time ], 
                    [ start_time, end_time ], 
                    ... 
                ]

            .. note::
                Start and end times of hitcircles are the same
        
        """
        all_times = StdMapData.all_times(map_data, flat=False)
        return np.asarray([ (hitobject_times[0], hitobject_times[-1]) for hitobject_times in all_times ])


    @staticmethod
    def get_idx_start_time(map_data, time):
        """
        Gets the index of the first hitobject that starts after the given time

        Parameters
        ----------
        map_data : numpy.array
            Map data to get the index of hitobject for

        time : int
            Time to get the index of hitobject for

        Returns
        -------
        int 
            index of hitobject in map data
        """
        if type(time) == type(None): return None

        times = np.asarray(StdMapData.start_times(map_data))
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))

    
    @staticmethod
    def get_idx_end_time(map_data, time):
        """
        Gets the index of the first hitobject that ends after the given time

        Parameters
        ----------
        map_data : numpy.array
            Map data to get the index of hitobject for

        time : int
            Time to get the index of hitobject for

        Returns
        -------
        int 
            index of hitobject in map data
        """
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