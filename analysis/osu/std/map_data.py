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

    TYPE_CIRCLE  = 1
    TYPE_SLIDER  = 2
    TYPE_SPINNER = 3

    IDX_TIME   = 0
    IDX_X      = 1
    IDX_Y      = 2
    IDX_TYPE   = 3
    IDX_OBJECT = 4

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
        aimpoint_data = []

        # Hit circle recording
        if std_hitobject.is_hitobject_type(Hitobject.CIRCLE):
            # Extract note timings
            note_start = std_hitobject.time
            note_end   = std_hitobject.time

            # Adjust note ending based on whether it is single or hold note (determined via min_press_duration)
            note_end = note_end if (note_end - note_start >= min_press_duration) else (note_start + min_press_duration)

            aimpoint_data.append(np.asarray([ note_start, std_hitobject.pos.x, std_hitobject.pos.y, StdMapData.TYPE_PRESS, StdMapData.TYPE_CIRCLE ]))
            aimpoint_data.append(np.asarray([ note_end, std_hitobject.pos.x, std_hitobject.pos.y, StdMapData.TYPE_RELEASE, StdMapData.TYPE_CIRCLE ]))
        
        # Slider recording
        elif std_hitobject.is_hitobject_type(Hitobject.SLIDER):
            aimpoint_times = std_hitobject.get_aimpoint_times()

            aimpoint_data.append(np.asarray([ aimpoint_times[0], std_hitobject.time_to_pos(aimpoint_times[0]).x, std_hitobject.time_to_pos(aimpoint_times[0]).y, StdMapData.TYPE_PRESS, StdMapData.TYPE_SLIDER ]))
            if len(aimpoint_times) > 2:
                for aimpoint_time in aimpoint_times[1:-1]:
                    aimpoint_data.append(np.asarray([ aimpoint_time, std_hitobject.time_to_pos(aimpoint_time).x, std_hitobject.time_to_pos(aimpoint_time).y, StdMapData.TYPE_HOLD, StdMapData.TYPE_SLIDER ]))
            aimpoint_data.append(np.asarray([ aimpoint_times[-1], std_hitobject.time_to_pos(aimpoint_times[-1]).x, std_hitobject.time_to_pos(aimpoint_times[-1]).y, StdMapData.TYPE_RELEASE, StdMapData.TYPE_SLIDER ]))

        # Convert the dictionary of recorded timings and states into a pandas data
        return pd.DataFrame(aimpoint_data, columns=['time', 'x', 'y', 'type', 'object'])


    @staticmethod
    def get_map_data(std_hitobjects):
        """
        .. note::
            This function is intended to be used directly

        .. warning::
            Some hitobject indices may not be present. These are hitobjects that are not processed and
            ommited from map data. It is recommended to use StdMapData.get_next_hitobject_idx to get index
            that follows

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
                                            x      y  type
                hitobject time                            
                0         494.0    256.000000  192.0   1.0
                          495.0    256.000000  192.0   3.0
                1         994.0    256.000000  192.0   1.0
                          995.0    256.000000  192.0   3.0
                2         1494.0   256.000000  192.0   1.0
                ...                      ...    ...   ...
                48        49494.0  302.027397   32.0   2.0
                          49994.0  160.000000   32.0   3.0
                49        49494.0  320.000000   32.0   1.0
                          49994.0  174.027397   32.0   2.0
                          50494.0   32.000000   32.0   3.0

                [109 rows x 3 columns]
        """
        map_data = []
        for hitobject in std_hitobjects:
            map_data.append(StdMapData.std_hitobject_to_aimpoints(hitobject))

        return pd.concat(map_data, axis=0, keys=range(len(map_data)), names=[ 'hitobject', 'aimpoint' ])


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
        return map_data[map_data.values[:, StdMapData.IDX_TYPE] == StdMapData.TYPE_PRESS]


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
        return map_data[map_data.values[:, StdMapData.IDX_TYPE] == StdMapData.TYPE_RELEASE]



    @staticmethod
    def get_objects(map_data):
        """
        Gets list of hitobjects types

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
                    ... N hitobjects
                ]
        """
        return map_data.values[:, StdMapData.IDX_OBJECT][map_data.values[:, StdMapData.IDX_TYPE] == StdMapData.TYPE_PRESS]


    @staticmethod
    def get_visible_at(map_data, time, ar_ms):
        """
        Gets number of hitobjects visible at time `time` given `ar_ms`

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on
        
        time : int
            Time to determine which hitobject are visible at
        
        ar_ms : int
            AR of map in milliseconds

        Returns
        -------
        int
        number of hitobjects in the map
        """
        releases = StdMapData.get_releases(map_data).values
        presses  = StdMapData.get_presses(map_data).values

        visible = ((time - ar_ms) < releases[:, StdMapData.IDX_TIME]) & (presses[:, StdMapData.IDX_TIME] <= time)
        visible = np.arange(len(presses))[visible]
        
        return map_data.loc[visible]


    @staticmethod
    def get_scorepoint_before(map_data, time):
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
                x       207.609756
                y       192.000000
                type      3.000000
                Name: (8, 11994.0), dtype: float64
        """
        try: return map_data[map_data['time'] < time].iloc[-1]
        except IndexError: return None


    @staticmethod
    def get_scorepoint_after(map_data, time):
        """
        Get the closest scorepoint right after the desired point in time

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
                x       207.609756
                y       192.000000
                type      3.000000
                Name: (8, 11994.0), dtype: float64
        """
        try: return map_data[map_data['time'] > time].iloc[0]
        except IndexError: return None


    @staticmethod
    def get_next_hitobject_idx(map_data, idx):
        """
        Gets the next hitobject index, automatically handling indexes for 
        hitobjects that are not handled in map data.

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on

        idx : int
            Index to get after this one

        Returns
        -------
        int
        Hitobject index following ``idx``, or number of hitobject there are, which ever is smaller
        """
        while True:
            idx += 1
            if idx >= len(map_data): 
                return len(map_data)
            
            try: map_data.loc[idx]
            except: continue
            else: break

        return idx
        

    @staticmethod
    def get_note_before(map_data, time):
        """
        Get the closest note right before the desired point in time

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on
        
        time : int
            Desired point in time

        Returns
        -------
        numpy.array
            note data
            ::
                            x      y  type
                time                      
                1494.0  256.0  192.0   1.0
                1495.0  256.0  192.0   3.0
        """
        try:
            # Type == Press is needed to handle overlapping sliders
            before_filter = map_data['time'] < time
            press_filter  = map_data['type'] == StdMapData.TYPE_PRESS
            idx = map_data[before_filter & press_filter].index[-1][0]
            return map_data.loc[idx]
        except IndexError: return None


    @staticmethod
    def get_note_after(map_data, time):
        """
        Get the closest note right after the desired point in time

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on
        
        time : int
            Desired point in time

        Returns
        -------
        numpy.array
            note data
            ::
                            x      y  type
                time                      
                1494.0  256.0  192.0   1.0
                1495.0  256.0  192.0   3.0
        """
        try:
            # Type == Press is needed to handle overlapping sliders
            after_filter = map_data['time'] > time
            press_filter = map_data['type'] == StdMapData.TYPE_PRESS
            idx = map_data[after_filter & press_filter].index[0][0]
            return map_data.loc[idx]
        except IndexError: return None


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
        return map_data.values[map_data.values[:, StdMapData.IDX_TYPE] == StdMapData.TYPE_PRESS][:, StdMapData.IDX_TIME]


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
        return map_data.values[map_data.values[:, StdMapData.IDX_TYPE] == StdMapData.TYPE_RELEASE][:, StdMapData.IDX_TIME]


    @staticmethod
    def all_times(map_data):
        """
        Gets time data for all scorepoint in the map

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
        return map_data.values[:, StdMapData.IDX_TIME]


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
        all_times = StdMapData.all_times(map_data)
        if exclusive:
            time_slice = (start_time < all_times) & (all_times < end_time)
        else:
            time_slice = (start_time <= all_times) & (all_times <= end_time)

        return map_data[time_slice]


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
        presses = map_data.values[map_data.values[:, StdMapData.IDX_TYPE] == StdMapData.TYPE_PRESS]
        return presses[:, StdMapData.IDX_X], presses[:, StdMapData.IDX_Y]

    
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
        releases = map_data.values[map_data.values[:, StdMapData.IDX_TYPE] == StdMapData.TYPE_RELEASE]
        return releases[:, StdMapData.IDX_X], releases[:, StdMapData.IDX_Y]


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
        return map_data.values[:, StdMapData.IDX_X], map_data.values[:, StdMapData.IDX_Y]