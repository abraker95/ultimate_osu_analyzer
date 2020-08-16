import numpy as np
import pandas as pd
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
    POSX = 1
    POSY = 2
    TYPE = 3

    TYPE_PRESS   = 1
    TYPE_HOLD    = 2
    TYPE_RELEASE = 3

    @staticmethod 
    def std_hitobject_to_aimpoints(std_hitobject, min_press_duration=1):
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
                    [ aimpoint_x, aimpoint_y, type ],
                    [ aimpoint_x, aimpoint_y, type ],
                    ... N aimpoints
                ]

            Hitcircles contain only one scorepoint. Sliders can contain
            more than one. This format is reflected in the groups of 
            [ time, pos ] in the map data
        """
        # Record data via dictionary to identify unique timings
        aimpoint_data = {}

        # Hit circle recording
        if std_hitobject.is_hitobject_type(Hitobject.CIRCLE):
            # Extract note timings
            note_start = std_hitobject.time
            note_end   = std_hitobject.time

            # Adjust note ending based on whether it is single or hold note (determined via min_press_duration)
            note_end = note_end if (note_end - note_start >= min_press_duration) else (note_start + min_press_duration)

            aimpoint_data[note_start] = np.asarray([ std_hitobject.pos.x, std_hitobject.pos.y, StdMapData.TYPE_PRESS ])
            aimpoint_data[note_end]   = np.asarray([ std_hitobject.pos.x, std_hitobject.pos.y, StdMapData.TYPE_RELEASE ])
        
        # Slider recording
        elif std_hitobject.is_hitobject_type(Hitobject.SLIDER):
            aimpoint_times = std_hitobject.get_aimpoint_times()

            aimpoint_data[aimpoint_times[0]] = np.asarray([ std_hitobject.time_to_pos(aimpoint_times[0]).x, std_hitobject.time_to_pos(aimpoint_times[0]).y, StdMapData.TYPE_PRESS ])
            if len(aimpoint_times) > 2:
                for aimpoint_time in aimpoint_times[1:-1]:
                    aimpoint_data[aimpoint_time] = np.asarray([ std_hitobject.time_to_pos(aimpoint_time).x, std_hitobject.time_to_pos(aimpoint_time).y, StdMapData.TYPE_HOLD ])
            aimpoint_data[aimpoint_times[-1]] = np.asarray([ std_hitobject.time_to_pos(aimpoint_times[-1]).x, std_hitobject.time_to_pos(aimpoint_times[-1]).y, StdMapData.TYPE_RELEASE ])

        # Sort data by timings
        aimpoint_data = dict(sorted(aimpoint_data.items()))

        # Convert the dictionary of recorded timings and states into a pandas data
        aimpoint_data = pd.DataFrame.from_dict(aimpoint_data, orient='index', columns=['x', 'y', 'type'])
        return aimpoint_data


    @staticmethod
    def get_map_data(std_hitobjects):
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
                    [ time, aimpoint_x, aimpoint_y, type ],
                    [ time, aimpoint_x, aimpoint_y, type ],
                    ... N aimpoints
                ]
        """
        map_data = []
        for hitobject in std_hitobjects:
            map_data.append(StdMapData.std_hitobject_to_aimpoints(hitobject))

        return pd.concat(map_data, axis=0, keys=range(len(map_data)), names=[ 'hitobject', 'time' ])


    @staticmethod
    def get_num_hitobjects(map_data):
        """
        Gets number of hitobjects in the map

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on
        
        Returns
        -------
        int
        number of hitobjects in the map
        """
        return len(np.bincount(map_data.index.get_level_values('hitobject').values.astype(np.int32)))


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
                    [ aimpoint_x, aimpoint_y, type ],
                    [ aimpoint_x, aimpoint_y, type ],
                    ... N aimpoints
                ]
        """
        return map_data.query(f'type == {StdMapData.TYPE_PRESS}')


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
                    [ aimpoint_x, aimpoint_y, type ],
                    [ aimpoint_x, aimpoint_y, type ],
                    ... N aimpoints
                ]
        """
        return map_data.query(f'type == {StdMapData.TYPE_RELEASE}')


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
        try: return map_data.query(f'time < {time}').iloc[-1]
        except IndexError: return None


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
                [ time, aimpoint_x, aimpoint_y, type ]
            
        """
        try: return map_data.query(f'time > {time}').iloc[0]
        except IndexError: return None


    @staticmethod
    def time_slice(map_data, start_time, end_time, exclusive=True):
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
                [          
                    [ time, aimpoint_x, aimpoint_y, type ]
                    [ time, aimpoint_x, aimpoint_y, type ]
                    ...
                ]
            
        """
        eq = '' if exclusive else '='
        return map_data.query(f'{start_time} <{eq} time <{eq} {end_time}')


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
        return map_data.query(f'type == {StdMapData.TYPE_PRESS}').index.get_level_values('time').values


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
        return map_data.query(f'type == {StdMapData.TYPE_RELEASE}').index.get_level_values('time').values


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
        return map_data.index.get_level_values('time').values


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
                    [ aimpoint_x, aimpoint_y ], 
                    [ aimpoint_x, aimpoint_y ], 
                    ... 
                ]
            
        """
        presses = map_data.query(f'type == {StdMapData.TYPE_PRESS}')
        return presses['x'].values, presses['y'].values

    
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
                    [ aimpoint_x, aimpoint_y ], 
                    [ aimpoint_x, aimpoint_y ], 
                    ... 
                ]
            
        """
        releases = map_data.query(f'type == {StdMapData.TYPE_RELEASE}')
        return releases['x'].values, releases['y'].values


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
                    [ aimpoint_x, aimpoint_y ], 
                    [ aimpoint_x, aimpoint_y ], 
                    ... 
                ]
        """
        return map_data['x'].values, map_data['y'].values