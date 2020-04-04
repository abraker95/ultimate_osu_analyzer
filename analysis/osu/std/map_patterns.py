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
    def detect_short_sliders(map_data, cs_px):
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
        start_positions = StdMapData.start_positions(map_data)
        end_positions   = StdMapData.end_positions(map_data)

        # TODO: Aimpoints in between slider ends are being ignored. That can make a long slider
        # marked as a short one. This function was inteaded to be used to determine whether to
        # take hitobject's starting time or ending time, but this complicates things. Aimpoints need
        # to be iterated through and determined if each if far enough from the next that they can
        # be skipped.

        dists = lambda x1, x2, y1, y2: np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        data  = end_positions[:, 0], start_positions[:, 0], end_positions[:, 1], start_positions[:, 1]
        return dists(*data) < cs_px


    @staticmethod
    def reinterpret_short_sliders(map_data, cs_px):
        """
        Makes short sliders single notes if they are short enough

        .. note::
            Use StdMapData.start_times to correlate mask with hitobject timing

        .. note::
            Makes a copy of the map data

        Parameters
        ----------
        map_data : numpy.array
            Map data to operate on

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
        start_time_idxs  = np.where(map_data[:, StdMapData.TYPE] == StdMapData.TYPE_PRESS)[0]
        end_time_idxs    = np.where(map_data[:, StdMapData.TYPE] == StdMapData.TYPE_RELEASE)[0]
        is_short_sliders = StdMapPatterns.detect_short_sliders(map_data, cs_px)
        new_map_data     = []

        for data in zip(start_time_idxs, end_time_idxs, is_short_sliders):
            start_time_idx, end_time_idx, is_short_slider = data
            hitobject_data = map_data[start_time_idx : end_time_idx + 1]

            if is_short_slider:
                press   = hitobject_data[0].copy()
                release = hitobject_data[0].copy()
                release[StdMapData.TYPE] = StdMapData.TYPE_RELEASE
                
                new_map_data.append(press)
                new_map_data.append(release)
                continue
            
            for aimpoint in hitobject_data:
                new_map_data.append(aimpoint.copy())

        return np.asarray(new_map_data)

