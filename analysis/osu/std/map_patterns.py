import numpy as np

from misc.geometry import *
from misc.math_utils import *
from misc.metrics import Metrics

from osu.local.beatmap.beatmap import Beatmap

from analysis.osu.std.map_data import StdMapData



class StdMapPatterns():
    """
    Class used for pattern processing and recognition

    .. warning::
        Undocumented functions in this class are not supported and are experimental.
    """
    
    @staticmethod
    def detect_short_sliders_dist(map_data, cs_px):
        """
        Returns a True/False mask indicating whether the hitobject's ends are short enough to not
        require the player to move their mouse to complete.

        .. note::
            Use StdMapData.start_times to correlate mask with hitobject timing

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on

        cs_px : float
            Circle size of the map, in osu!px

        Returns
        -------
        numpy.array
            Masked boolean data
            ::
                [ bool, bool, bool ]
        """
        presses = StdMapData.get_presses(map_data).values
        releases = StdMapData.get_releases(map_data).values

        # TODO: Aimpoints in between slider ends are being ignored. That can make a long slider
        # marked as a short one. This function was inteaded to be used to determine whether to
        # take hitobject's starting time or ending time, but this complicates things. Aimpoints need
        # to be iterated through and determined if each if far enough from the next that they can
        # be skipped.

        xs = presses[:, StdMapData.IDX_X]
        xe = releases[:, StdMapData.IDX_X]
        ys = presses[:, StdMapData.IDX_Y]
        ye = releases[:, StdMapData.IDX_Y]

        dists = lambda xs, xe, ys, ye: np.sqrt((xe - xs)**2 + (ye - ys)**2)
        return dists(xs, xe, ys, ye) < cs_px


    @staticmethod
    def detect_short_sliders_time(map_data, min_time):
        """
        Returns a True/False mask indicating whether the slider is brief enough to not
        require the player to need to be held

        .. note::
            Use StdMapData.start_times to correlate mask with hitobject timing

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on

        min_time : int
            Minimum slider time in ms. Sliders lasting shorter than this are considered to be hitcircles

        Returns
        -------
        numpy.array
            Masked boolean data
            ::
                [ bool, bool, bool ]
        """
        presses = StdMapData.get_presses(map_data).values
        releases = StdMapData.get_releases(map_data).values

        return ((releases[:, StdMapData.IDX_TIME] - presses[:, StdMapData.IDX_TIME]) < min_time)


    @staticmethod
    def reinterpret_short_sliders(map_data, min_time, cs_px):
        """
        Makes short sliders single notes if they are short enough

        .. note::
            Use StdMapData.start_times to correlate mask with hitobject timing

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on

        min_time : float
            Min hold time of a slider

        cs_px : float
            Circle size of the map, in osu!px

        Returns
        -------
        numpy.array
            Map data representing the following format:
            ::
                [
                    [ start_time, aimpoint_x, aimpoint_y, type ],
                    [ start_time, aimpoint_x, aimpoint_y, type ],
                    ... N aimpoints
                ]
        """
        is_short_sliders_time = StdMapPatterns.detect_short_sliders_time(map_data, min_time)
        is_short_sliders_dist = StdMapPatterns.detect_short_sliders_dist(map_data, cs_px)

        map_data = map_data.copy()

        short_sliders_idxs = np.arange(len(is_short_sliders_time))[is_short_sliders_time | is_short_sliders_dist]
        for short_sliders_idx in short_sliders_idxs:
            map_data.loc[short_sliders_idx].drop(map_data.loc[short_sliders_idx].index[1:], inplace=True)

        # TODO: Get this working

        return map_data
    