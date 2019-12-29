import numpy as np
import itertools

from osu.local.hitobject.hitobject import Hitobject
from osu.local.hitobject.std.std import Std
from misc.numpy_utils import NumpyUtils



class StdReplayData():
    """
    Class used for navigating, extracting, and operating on standard gamemode replay data.
    
    .. note::
        This is not to be confused with the replay data in the osu.local.replay.replay.Replay class.
        Data used by this class is in numpy array form. Data in the Replay 
        class is based on *.osr file structure and is not in a friendly 
        format to perform analysis on.
    """

    TIME  = 0   # [ int ]   Time of event
    XPOS  = 1   # [ float ] Cursor's x-position
    YPOS  = 2   # [ float ] Cursor's y-position
    M1    = 3   # [ bool ]  Mouse 1 button flag
    M2    = 4   # [ bool ]  Mouse 2 button flag
    K1    = 5   # [ bool ]  Keyboard 1 button flag
    K2    = 6   # [ bool ]  Keyboard 2 button flag
    SMOKE = 7   # [ bool ]  Smoke button flag

    @staticmethod 
    def get_replay_data(replay_events):
        """
        Gets replay data

        Parameters
        ----------
        replay_events : list
            Replay event data located in ``Replay.play_data``
        
        Returns
        -------
        numpy.array
            List of events with data on time, positions of cursor, and flags on 
            various key presses in the following format:
            ::
                [
                    [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
                    [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
                    [ time, x_pos, y_pos, m1, m2, k1, k2, smoke ],
                    ...  N events
                ]
        """
        replay_data = []

        m1_mask    = (1 << 0)
        m2_mask    = (1 << 1)
        k1_mask    = (1 << 2)
        k2_mask    = (1 << 3)
        smoke_mask = (1 << 4)

        for replay_event in replay_events:
            # "and not" because K1 is always used with M1; K2 is always used with M2. So make sure keys are not pressed along with mouse
            k1_pressed    = ((replay_event.keys_pressed & k1_mask) > 0)
            k2_pressed    = ((replay_event.keys_pressed & k2_mask) > 0) 
            m1_pressed    = ((replay_event.keys_pressed & m1_mask) > 0) and not k1_pressed
            m2_pressed    = ((replay_event.keys_pressed & m2_mask) > 0) and not k2_pressed
            smoke_pressed = (replay_event.keys_pressed & smoke_mask) > 0

            event = [ replay_event.t, replay_event.x, replay_event.y, m1_pressed, m2_pressed, k1_pressed, k2_pressed, smoke_pressed ]
            replay_data.append(event)

        return np.asarray(replay_data)


    @staticmethod
    def component_data(replay_data, component):
        """
        Gets a specific component of replay data. This function
        is serves as an alias for ``replay_data[:, component]``

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        component : int
            Which component to get data for. Components are:
                - ``StdReplayData.TIME``  - List of all cursor times
                - ``StdReplayData.XPOS``  - List of all cursor x coordinate positions
                - ``StdReplayData.YPOS``  - List of all cursor y coordinate positions
                - ``StdReplayData.M1``    - List of all mouse button 1 presses
                - ``StdReplayData.M2``    - List of all mouse button 2 presses
                - ``StdReplayData.K1``    - List of all keyboard key 1 presses
                - ``StdReplayData.K2``    - List of all keyboard key 2 presses
                - ``StdReplayData.SMOKE`` - List of all smoke key presses
        
        Returns
        -------
        numpy.array
            Replay component data
        """
        return replay_data[:, component]


    @staticmethod
    def order_timings(replay_data):
        """
        Sometimes replay data has jumps in timing going backwards. This orders replay
        frames into correct sequence

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        Returns
        -------
        numpy.array
            Replay data sorted by chronological order
        """
        return replay_data[np.argsort(replay_data[:, 0]), :]


    @staticmethod
    def interpolate_timings(replay_data):
        """
        Replay data is often eradic with its timings due to sync issues in osu! client 
        dealing with performance. The frames do not occur a constant interval after another,
        and can range to have between 1ms and 25ms difference. This makes the data have
        an average sample rate of the data given.

        Parameters
        ----------
        replay_data : numpy.array
            Input replay data

        Returns
        -------
        numpy.array
            Replay data with average sample rate of `replay_data`
        """
        avg_dt = np.mean(np.diff(replay_data[:, 0]))                       # Average differences in times between frames
        eq_t   = avg_dt*np.arange(1, len(replay_data)) + replay_data[0,0]  # Equalized timings between franes

        t = np.concatenate(([ replay_data[0, 0] ], eq_t))
        return np.hstack([np.asarray([t]).T, replay_data[:, 1:] ])


    @staticmethod
    def press_start_times(replay_data, key=None):
        """        
        Tuple with indices in replay_data where a press ends and timings where press ends.
        ``press_start_idxs`` can be used on original ``replay_data`` to get full data related to start times
        like so: ``replay_data[press_start_idxs]``

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        key : int
            Which key to get start times for. If ``key is None``, then intermixed key start times
            for ``M1``, ``M2``, ``K1``, and ``K2`` are returned.
                - ``StdReplayData.M1``    - Mouse button 1 presses
                - ``StdReplayData.M2``    - Mouse button 2 presses
                - ``StdReplayData.K1``    - Keyboard key 1 presses
                - ``StdReplayData.K2``    - Keyboard key 2 presses
                - ``StdReplayData.SMOKE`` - Smoke key presses
        Returns
        -------
        numpy.array
            Format:
            ::
                [ press_start_idxs, press_start_times ]
            which is
            ::
                [ [ int, int, ... ], [ int, int, ... ] ]
        """
        replay_data = np.asarray(replay_data)
        
        if key == None:
            m1_idxs, m1_press_start_times = StdReplayData.press_start_times(replay_data, StdReplayData.M1)
            m2_idxs, m2_press_start_times = StdReplayData.press_start_times(replay_data, StdReplayData.M2)
            k1_idxs, k1_press_start_times = StdReplayData.press_start_times(replay_data, StdReplayData.K1)
            k2_idxs, k2_press_start_times = StdReplayData.press_start_times(replay_data, StdReplayData.K2)

            press_start_times = np.concatenate((m1_press_start_times, m2_press_start_times, k1_press_start_times, k2_press_start_times))
            press_idxs        = np.concatenate((m1_idxs, m2_idxs, k1_idxs, k2_idxs))

            sort_idxs = np.argsort(press_start_times, axis=None)
            return np.asarray([ press_idxs[sort_idxs], press_start_times[sort_idxs] ])
        else:
            times    = StdReplayData.component_data(replay_data, StdReplayData.TIME)
            key_data = StdReplayData.component_data(replay_data, key)

            key_changed = (key_data[1:] != key_data[:-1])
            key_changed = np.insert(key_changed, 0, 0)
            is_hold     = (key_data == 1)

            press_start_mask  = np.logical_and(key_changed, is_hold)
            press_start_times = times[press_start_mask]

            return np.asarray([ np.where(press_start_mask == 1)[0], press_start_times ])


    @staticmethod
    def press_end_times(replay_data, key=None):
        """        
        Tuple with indices in replay_data where a press ends and timings where press ends.
        ``press_end_idxs`` can be used on original ``replay_data`` to get full data related to end times
        like so: ``replay_data[press_end_idxs]``

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        key : int
            Which key to get start times for. If key = None, then intermixed key start times
            for ``M1``, ``M2``, ``K1``, and ``K2`` are returned.
                - ``StdReplayData.M1``    - Mouse button 1 presses
                - ``StdReplayData.M2``    - Mouse button 2 presses
                - ``StdReplayData.K1``    - Keyboard key 1 presses
                - ``StdReplayData.K2``    - Keyboard key 2 presses
                - ``StdReplayData.SMOKE`` - Smoke key presses

        Returns
        -------
        numpy.array
            Format:
            ::
                [ press_end_idxs, press_end_times ]
            which is
            ::
                [ [ int, int, ... ], [ int, int, ... ] ]
        """
        replay_data = np.asarray(replay_data)

        if key == None:
            m1_idxs, m1_press_end_times = StdReplayData.press_end_times(replay_data, StdReplayData.M1)
            m2_idxs, m2_press_end_times = StdReplayData.press_end_times(replay_data, StdReplayData.M2)
            k1_idxs, k1_press_end_times = StdReplayData.press_end_times(replay_data, StdReplayData.K1)
            k2_idxs, k2_press_end_times = StdReplayData.press_end_times(replay_data, StdReplayData.K2)

            press_end_times = np.concatenate((m1_press_end_times, m2_press_end_times, k1_press_end_times, k2_press_end_times))
            press_idxs      = np.concatenate((m1_idxs, m2_idxs, k1_idxs, k2_idxs))

            sort_idxs = np.argsort(press_end_times, axis=None)
            return np.asarray([ press_idxs[sort_idxs], press_end_times[sort_idxs] ])
        else:
            times    = StdReplayData.component_data(replay_data, StdReplayData.TIME)
            key_data = StdReplayData.component_data(replay_data, key)

            key_changed = (key_data[1:] != key_data[:-1])
            key_changed = np.insert(key_changed, 0, 0)
            is_not_hold = (key_data == 0)

            press_end_mask  = np.logical_and(key_changed, is_not_hold)
            press_end_times = times[press_end_mask]
            
            return np.asarray([ np.where(press_end_mask == 1)[0], press_end_times ])

    
    @staticmethod
    def press_start_end_times(replay_data, key=None):
        """
        Tuple with indices in ``replay_data`` where a press starts and ends and timings where press 
        stars and ends. ``press_start_end_idxs`` can be used on original ``replay_data`` to get full data 
        related to end times like so: ``replay_data[press_start_end_idxs]``

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        key : int
            Which key to get start times for. If ``key is None``, then intermixed key start times
            for ``M1``, ``M2``, ``K1``, and ``K2`` are returned.
                - ``StdReplayData.M1``    - Mouse button 1 presses
                - ``StdReplayData.M2``    - Mouse button 2 presses
                - ``StdReplayData.K1``    - Keyboard key 1 presses
                - ``StdReplayData.K2``    - Keyboard key 2 presses
                - ``StdReplayData.SMOKE`` - Smoke key presses

        Returns
        -------
        numpy.array
            Format:
            ::
                [ 
                    [ press_start_idx, press_start_time, press_end_idx, press_end_time ],
                    [ press_start_idx, press_start_time, press_end_idx, press_end_time ],
                    ...
                ]
        """
        press_start_idx, press_start_times = StdReplayData.press_start_times(replay_data, key)
        press_end_idx, press_end_times     = StdReplayData.press_end_times(replay_data, key)

        return np.asarray(list(zip(press_start_idx, press_start_times, press_end_idx, press_end_times)))


    @staticmethod
    def get_idx_time(replay_data, time):
        """
        Gets index of first sample in ``replay_data`` where time of sample is greater than ``time``
        
        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        time : int
            Time in replay data

        Returns
        -------
        int
        """
        event_times = replay_data[:,StdReplayData.TIME]

        idx = np.where(event_times >= time)[0]
        idx = (event_times.size - 1) if idx.size == 0 else min(idx[0] + 1, event_times.size - 1)

        return idx

    
    @staticmethod
    def get_idx_press_start_time(replay_data, time, key=None):
        """
        Gets index of closest press of ``key`` to ``time`` in ``replay_data``

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        time : int
            Time in replay data

        key : int
            Keyboard key/Mouse button to get starting time of press for

        Returns
        -------
        int
        """
        if not time: return None

        times = StdReplayData.press_start_times(replay_data, key)
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))


    @staticmethod
    def get_idx_press_end_time(replay_data, time, key=None):
        """
        Gets index of closest release of ``key`` to ``time`` in ``replay_data``

        Parameters
        ----------
        replay_data : numpy.array
            Replay data

        time : int
            Time in replay data

        key : int
            Keyboard key/Mouse button to get ending time of press for

        Returns
        -------
        int
        """
        if not time: return None

        times = StdReplayData.press_end_times(replay_data, key)
        return min(max(0, np.searchsorted(times, [time], side='right')[0] - 1), len(times))