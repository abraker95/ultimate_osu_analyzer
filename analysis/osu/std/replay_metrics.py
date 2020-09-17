import numpy as np

from misc.geometry import *
from misc.numpy_utils import NumpyUtils

from osu.local.beatmap.beatmap import Beatmap
from analysis.osu.std.replay_data import StdReplayData



class StdReplayMetrics():
    """
    Class used for analyzing replay data.
    """

    @staticmethod
    def cursor_velocity(replay_data):
        """
        Absolute cursor velocity

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        Returns
        -------
        tuple
            A pair of time and cursor velocity data.
            Size of resultant data is ``len(replay_data) - 1``
            ::
                ( times, vel )
        """
        replay_data = replay_data.values
        all_times = replay_data[:, 0]
        if len(all_times) < 2: return [], []
        
        vels = np.sqrt(np.diff(replay_data[:, 1])**2 + np.diff(replay_data[:, 2])**2)/np.diff(all_times)
        return all_times[2:], vels[1:]


    @staticmethod
    def cursor_acceleration(replay_data):
        """       
        Absolute cursor acceleration

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        Returns
        -------
        tuple
            A pair of time and cursor acceleration data. 
            Size of resultant data is ``len(replay_data) - 2``
            ::
                ( times, accel )
        """
        cursor_velocity = StdReplayMetrics.cursor_velocity(replay_data)
        times, velocities = cursor_velocity

        if len(times) < 2: return [], []
        intervals = np.diff(times)
        
        accel = (velocities[1:] - velocities[:-1])/intervals
        return times, accel[1:]


    @staticmethod
    def cursor_jerk(replay_data):
        """
        Absolute cursor jerk

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        Returns
        -------
        tuple
            A pair of time and cursor jerk data. 
            Size of resultant data is ``len(replay_data) - 3``
            ::
                ( times, jerk )
        """
        cursor_acceleration  = StdReplayMetrics.cursor_acceleration(replay_data)
        times, accelerations = cursor_acceleration

        if len(times) < 2: return [], []
        intervals = np.diff(times)
        
        jerk = (accelerations[1:] - accelerations[:-1])/intervals
        return times, jerk[1:]


    @staticmethod
    def cursor_vel_xy(replay_data):
        """
        Parametric cursor velocity

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        Returns
        -------
        tuple
            A pair of time and parametric cursor velocity data. 
            Size of resultant data is ``len(replay_data) - 1``
            ::
                ( times, vel_x, vel_y )
        """
        all_times     = replay_data[:,0]
        all_positions = np.asarray(list(zip(replay_data[:,1], replay_data[:,2])))

        if len(all_times) < 2: return [], []
        
        dx = np.diff(all_positions[:,0])
        dy = np.diff(all_positions[:,1])
        dt = np.diff(all_times)
        
        return all_times[1:], dx/dt, dy/dt


    @staticmethod
    def cursor_accel_xy(replay_data):
        """
        Parametric cursor acceleration

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        Returns
        -------
        tuple
            A pair of time and parametric cursor acceleration data. 
            Size of resultant data is ``len(replay_data) - 2``
            ::
                ( times, accel_x, accel_y )
        """
        cursor_vel_xy       = StdReplayMetrics.cursor_vel_xy(replay_data)
        times, vel_x, vel_y = cursor_vel_xy

        if len(times) < 2: return [], []
        
        dvx = np.diff(vel_x)
        dvy = np.diff(vel_y)
        dt = np.diff(times)
        
        return times[1:], dvx/dt, dvy/dt


    @staticmethod
    def cursor_jerk_xy(replay_data):
        """
        Parametric cursor jerk

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        Returns
        -------
        tuple
            A pair of time and parametric cursor jerk data. 
            Size of resultant data is ``len(replay_data) - 3``
            ::
                ( times, jerk_x, jerk_y )
        """
        cursor_accel_xy         = StdReplayMetrics.cursor_accel_xy(replay_data)
        times, accel_x, accel_y = cursor_accel_xy

        if len(times) < 2: return [], []
        
        dax = np.diff(accel_x)
        day = np.diff(accel_y)
        dt = np.diff(times)
        
        return times[1:], dax/dt, day/dt


    @staticmethod
    def press_intervals(replay_data):
        """
        List of intermixed press intervals for all keys

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        Returns
        -------
        tuple
            A pair of time and key press interval data
            ::
                ( times, intervals )
        """
        press_release_times = StdReplayData.press_start_end_times(replay_data)
        intervals = press_release_times[:,3] - press_release_times[:,1]
        
        return press_release_times[:,3], intervals



    @staticmethod
    def avg_cursor_pos(replay_data_list):
        """
        Takes all replays and determines average cursor position throughout all points in time
        Cursor positions are averaged across a moving average of 16 ms

        Parameters
        ----------
        replay_data_list : numpy.array
            List of replay datas

        Returns
        -------
        tuple
            Averaged cursor position data
            ::
                [
                    ( times, pos_x, pos_y ),
                    ( times, pos_x, pos_y ),
                    ...
                ]
        """
        #print('Flattening arrays')

        # Flatten all the replays into a list of frames
        replay_numpy_list = []
        for replay in replay_data_list:
            replay_numpy_list += replay
        replay_numpy_list = np.asarray(replay_numpy_list)

        replay_times = replay_numpy_list[:, StdReplayData.TIME]
        data = []

        #print('Flattened arrays')

        # Moving average with 16 ms window
        AVG_WINDOW = 16

        # Iterate through time
        for t in range(AVG_WINDOW, int(np.amax(replay_times)), 16):
            # Get the duration window of replay frames to average
            filtered_range = np.where(np.logical_and(t - AVG_WINDOW <= replay_times, replay_times <= t))

            # Average the cursor positions in the duration window
            avg_x = np.mean(replay_numpy_list[filtered_range][:, StdReplayData.XPOS])
            avg_y = np.mean(replay_numpy_list[filtered_range][:, StdReplayData.YPOS])

            data.append([t, avg_x, avg_y])
            #print(data[-1])

        return np.asarray(data)
