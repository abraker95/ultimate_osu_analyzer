import numpy as np

from misc.geometry import *
from misc.numpy_utils import NumpyUtils

from osu.local.beatmap.beatmap import Beatmap

from analysis.osu.std.replay_data import StdReplayData



class StdReplayMetrics():

    @staticmethod
    def cursor_velocity(replay_data):
        all_times = replay_data[:,0]
        if len(all_times) < 2: return [], []
        
        vel = np.sqrt(np.diff(replay_data[:,1])**2 + np.diff(replay_data[:,2])**2)/np.diff(replay_data[:, 0])
        return all_times[1:], vel


    @staticmethod
    def cursor_acceleration(replay_data):
        cursor_velocity = StdReplayMetrics.cursor_velocity(replay_data)
        times, velocities = cursor_velocity

        if len(times) < 2: return [], []
        intervals = np.diff(times)
        
        accel = (velocities[1:] - velocities[:-1])/intervals
        return times[1:], accel


    @staticmethod
    def cursor_jerk(replay_data):
        cursor_acceleration  = StdReplayMetrics.cursor_acceleration(replay_data)
        times, accelerations = cursor_acceleration

        if len(times) < 2: return [], []
        intervals = np.diff(times)
        
        jerk = (accelerations[1:] - accelerations[:-1])/intervals
        return times[1:], jerk


    @staticmethod
    def cursor_vel_xy(replay_data):
        all_times     = replay_data[:,0]
        all_positions = np.asarray(list(zip(replay_data[:,1], replay_data[:,2])))

        if len(all_times) < 2: return [], []
        
        dx = np.diff(all_positions[:,0])
        dy = np.diff(all_positions[:,1])
        dt = np.diff(all_times)
        
        return all_times[1:], dx/dt, dy/dt


    @staticmethod
    def cursor_accel_xy(replay_data):
        cursor_vel_xy       = StdReplayMetrics.cursor_vel_xy(replay_data)
        times, vel_x, vel_y = cursor_vel_xy

        if len(times) < 2: return [], []
        
        dvx = np.diff(vel_x)
        dvy = np.diff(vel_y)
        dt = np.diff(times)
        
        return times[1:], dvx/dt, dvy/dt


    @staticmethod
    def cursor_jerk_xy(replay_data):
        cursor_accel_xy         = StdReplayMetrics.cursor_accel_xy(replay_data)
        times, accel_x, accel_y = cursor_accel_xy

        if len(times) < 2: return [], []
        
        dax = np.diff(accel_x)
        day = np.diff(accel_y)
        dt = np.diff(times)
        
        return times[1:], dax/dt, day/dt


    @staticmethod
    def press_intervals(replay_data):
        press_release_times = StdReplayData.press_start_end_times(replay_data)
        intervals = press_release_times[:,3] - press_release_times[:,1]
        
        return press_release_times[:,3], intervals
