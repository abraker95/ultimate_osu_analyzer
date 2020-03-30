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
    TYPE = 2

    TYPE_PRESS   = 0
    TYPE_HOLD    = 1
    TYPE_RELEASE = 2

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
            yield [ std_hitobject.time, np.asarray([ std_hitobject.pos.x, std_hitobject.pos.y ]), StdMapData.TYPE_PRESS ]
        
        elif std_hitobject.is_hitobject_type(Hitobject.SLIDER):
            aimpoint_times = std_hitobject.get_aimpoint_times()

            yield [ aimpoint_times[0], np.asarray([ std_hitobject.time_to_pos(aimpoint_times[0]).x, std_hitobject.time_to_pos(aimpoint_times[0]).y ]), StdMapData.TYPE_PRESS ]
            if len(aimpoint_times) > 2:
                for aimpoint_time in aimpoint_times[1:-1]:
                    yield [ aimpoint_time, np.asarray([ std_hitobject.time_to_pos(aimpoint_time).x, std_hitobject.time_to_pos(aimpoint_time).y ]), StdMapData.TYPE_HOLD ]
            yield [ aimpoint_times[-1], np.asarray([ std_hitobject.time_to_pos(aimpoint_times[-1]).x, std_hitobject.time_to_pos(aimpoint_times[-1]).y ]), StdMapData.TYPE_RELEASE ]


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
                    [ time, pos, type ],
                    [ time, pos, type ],
                    ... N aimpoints
                ]
        """
        return np.asarray([ aimpoint for hitobject in std_hitobjects for aimpoint in StdMapData.std_hitobject_to_aimpoints(hitobject) ])


    @staticmethod
    def get_presses(map_data):
        """
        Gets aimpoints associated with the player pressing a key

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on
        
        Returns
        -------
        numpy.array
            Map data representing the following format:
            ::
                [ 
                    [ time, pos, type ],
                    [ time, pos, type ],
                    ... N aimpoints
                ]
        """
        return map_data[map_data[:, StdMapData.TYPE] == StdMapData.TYPE_PRESS]


    @staticmethod
    def get_releases(map_data):
        """
        Gets aimpoints associated with the player releasing a key

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on
        
        Returns
        -------
        numpy.array
            Map data representing the following format:
            ::
                [ 
                    [ time, pos, type ],
                    [ time, pos, type ],
                    ... N aimpoints
                ]
        """
        return map_data[map_data[:, StdMapData.TYPE] == StdMapData.TYPE_RELEASE]


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
        return StdMapData.get_presses(map_data)[:, StdMapData.TIME]


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
        return StdMapData.get_releases(map_data)[:, StdMapData.TIME]


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
        return np.vstack(StdMapData.get_presses(map_data)[:, StdMapData.POS])

    
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
        return np.vstack(StdMapData.get_releases(map_data)[:, StdMapData.POS])


    @staticmethod
    def all_positions(map_data):
        """
        Gets positions data for all hitobjects in the map

        Parameters
        ----------
        map_data : numpy.array
            Map data to get position data for

        Returns
        -------
        numpy.array
            returns numpy array of scorepoint positions
            ::
                [ 
                    [ pos_x, pos_y ], 
                    [ pos_x, pos_y ], 
                    ... 
                ]
        """
        return np.vstack(map_data[:, StdMapData.POS])


    @staticmethod
    def all_times(map_data):
        """
        Gets time data for all hitobjects in the map

        Parameters
        ----------
        map_data : numpy.array
            Map data to get position data for

        Returns
        -------
        numpy.array
            Returns numpy array of scorepoint times
            ::
                [ time, time, time, ... ]
            
        """
        return map_data[:, StdMapData.TIME]

    
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
        start_times = StdMapData.start_times(map_data)
        end_times   = StdMapData.end_times(map_data)
        return np.asarray(list(zip(start_times, end_times)))


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


    @staticmethod
    def get_idx_start_time_2(map_data, time):
        if not time: return None

        times = np.asarray(StdMapData.start_times(map_data))
        return np.where(times >= time)[0][0]


    @staticmethod
    def get_idx_end_time_2(map_data, time):
        if not time: return None
            
        times = np.asarray(StdMapData.end_times(map_data))
        return np.where(times >= time)[0][0]



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