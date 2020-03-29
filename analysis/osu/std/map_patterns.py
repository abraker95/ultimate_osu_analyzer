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

        dists = lambda x, y: np.sqrt((end_positions[:, 0] - start_positions[:, 0])**2 + (end_positions[:, 1] - start_positions[:, 1])**2)
        return dists(start_positions, end_positions) >= cs_px


