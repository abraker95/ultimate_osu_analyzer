import numpy as np

from misc.geometry import *
from misc.numpy_utils import NumpyUtils

from osu.local.beatmap.beatmap import Beatmap

from analysis.osu.std.replay_data import StdReplayData



class StdReplayMetrics():


    @staticmethod
    def cursor_velocity(replay_data):
        replay_data = np.asarray(replay_data[2:])

        all_times     = replay_data[:,0]
        all_positions = np.asarray(list(zip(replay_data[:,1], replay_data[:,2])))

        if len(all_times) < 2: return [], []
        intervals = np.diff(all_times)
        
        vel = NumpyUtils.dists(all_positions[1:], all_positions[:-1])/intervals
        return all_times[1:], vel


    @staticmethod
    def cursor_acceleration(replay_data):
        replay_data = np.asarray(replay_data[2:])

        cursor_velocity   = StdReplayMetrics.cursor_velocity(replay_data)
        times, velocities = cursor_velocity

        if len(times) < 2: return [], []
        intervals = np.diff(times)
        
        accel = (velocities[1:] - velocities[:-1])/intervals
        return times[1:], accel


    @staticmethod
    def cursor_jerk(replay_data):
        replay_data = np.asarray(replay_data[2:])

        cursor_acceleration  = StdReplayMetrics.cursor_acceleration(replay_data)
        times, accelerations = cursor_acceleration

        if len(times) < 2: return [], []
        intervals = np.diff(times)
        
        jerk = (accelerations[1:] - accelerations[:-1])/intervals
        return times[1:], jerk


    @staticmethod
    def press_intervals(replay_data):
        replay_data = np.asarray(replay_data[2:])

        press_release_times = StdReplayData.press_start_end_times(replay_data)
        intervals = press_release_times[:,3] - press_release_times[:,1]
        
        return press_release_times[:,3], intervals