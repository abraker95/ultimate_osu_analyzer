import numpy as np
from scipy import signal

from misc.geometry import *
from misc.numpy_utils import NumpyUtils

from osu.local.beatmap.beatmap import Beatmap
from analysis.osu.mania.map_data import ManiaMapData
from analysis.osu.mania.action_data import ManiaActionData



class ManiaMapMetrics():

    """
    Raw metrics
    """
    @staticmethod
    def calc_press_rate(action_data, window_ms=1000):
        """
        Calculates presses per second across all columns within indicated ``window_ms`` of time

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaMapData.get_action_data``

        window_ms : int
            Duration in milliseconds for which actions are counted up

        Returns
        -------
        (numpy.array, numpy.array)
        Tuple of ``(times, aps)``. ``times`` are timings corresponding to recorded actions per second. 
            ``aps`` are actions per second at indicated time.
        """
        aps = []
        for i in range(len(action_data)):
            actions_in_range = ManiaActionData.get_actions_between(action_data, action_data[i, 0] - window_ms, action_data[i, 0])
            num_actions = ManiaActionData.count_actions(actions_in_range, ManiaActionData.PRESS)
            aps.append([ action_data[i, 0], 1000*num_actions/window_ms ])

        return np.asarray(aps)


    @staticmethod
    def calc_press_rate_col(action_data, col, window_ms=1000):
        """
        Calculates presses per second in the specified column within indicated ``window_ms`` of time

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaMapData.get_action_data``

        col : int
            Column to calculated presses per second for

        window_ms : int
            Duration in milliseconds for which actions are counted up

        Returns
        -------
        (numpy.array, numpy.array)
        Tuple of ``(times, aps)``. ``times`` are timings corresponding to recorded actions per second. 
            ``aps`` are actions per second at indicated time.
        """
        action_data = action_data[:, [0, col]]
        aps = []

        for i in range(len(action_data)):
            actions_in_range = ManiaActionData.get_actions_between(action_data, action_data[i, 0] - window_ms, action_data[i, 0])
            num_actions = ManiaActionData.count_actions(actions_in_range, ManiaActionData.PRESS)
            aps.append([ action_data[i, 0], 1000*num_actions/window_ms ])

        return np.asarray(aps)


    @staticmethod
    def calc_max_press_rate_per_col(action_data, window_ms=1000):
        """
        Takes which column has max presses per second within indicated ``window_ms`` of time

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaMapData.get_action_data``

        window_ms : int
            Duration in milliseconds for which actions are counted up

        Returns
        -------
        (numpy.array, numpy.array)
        Tuple of ``(times, max_aps_per_col)``. ``times`` are timings corresponding to recorded actions per second. 
            ``max_aps_per_col`` are max actions per second at indicated time.
        """
        keys = ManiaActionData.num_keys(action_data)
        max_aps_per_col = []

        for i in range(len(action_data)):
            aps_col = []
            for col in range(1, keys + 1):
                col_data = action_data[:, [0, col]]

                actions_in_range = ManiaActionData.get_actions_between(col_data, col_data[i, 0] - window_ms, col_data[i, 0])
                num_actions = ManiaActionData.count_actions(actions_in_range, ManiaActionData.PRESS)
                aps_col.append(1000*num_actions/window_ms)
            
            max_aps_per_col.append([ action_data[i, 0], max(aps_col) ])

        return np.asarray(max_aps_per_col)


    @staticmethod
    def detect_presses_during_holds(action_data):
        """
        Masks presses that occur when there is at least one hold in one of the columns

        This is useful for determining which presses are harder due to finger independence.
        Holds have a tendency to make affected fingers slower or less accurate to press.

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        numpy.array
        action_data mask of actions detected
        """
        press_mask = ManiaActionData.mask_actions(action_data, ManiaActionData.PRESS)

        press_mask_any = np.any(action_data[:, 1:] == ManiaActionData.PRESS, 1)
        hold_mask_any  = np.any(action_data[:, 1:] == ManiaActionData.HOLD, 1)
        press_and_hold = np.logical_and(press_mask_any, hold_mask_any)

        press_mask[:, 1:] = press_and_hold[:, None] * press_mask[:, 1:]
        return press_mask


    @staticmethod
    def detect_hold_notes(action_data):
        """
        Masks hold notes; removes single notes from data.

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        numpy.array
        action_data mask of actions detected
        """
        hold_note_mask = action_data.copy()

        # Get idx where presses and releases occur. This is 2D data: (timings, columns)
        where_release = np.where(np.isin(action_data[:, 1:], ManiaActionData.RELEASE))
        where_press   = np.where(np.isin(action_data[:, 1:], ManiaActionData.PRESS))

        # Operate per column (because idk how to make numpy operate on all columns like this)
        for col in range(ManiaActionData.num_keys(action_data)):
            # For current column, get where PRESS and RELEASE occur
            where_release_timing = where_release[0][where_release[1] == col]
            where_press_timing   = where_press[0][where_press[1] == col]

            # Get timings for those PRESS and RELEASE
            release_timings = action_data[where_release_timing][:,0]
            press_timings   = action_data[where_press_timing][:,0]

            # Filter out idx in where_release_timing and where_press_timing that are 1 or less ms apart
            hold_note_start_mask = (release_timings - press_timings) > 1
        
            # Since we want to also include HOLD actions, let's assign 2 to PRESS and RELEASE actions associated
            # with hold notes so everything else can later be easily filtered out.
            hold_note_mask[:, col + 1][where_release_timing[hold_note_start_mask]] = 2
            hold_note_mask[:, col + 1][where_press_timing[hold_note_start_mask]] = 2

            # Filter out everthing else
            hold_note_mask[:, col + 1][hold_note_mask[:, col + 1] != 2] = 0

            # Set all the 2's to 1's
            hold_note_mask[:, col + 1][hold_note_mask[:, col + 1] == 2] = 1

        return hold_note_mask


    @staticmethod
    def data_to_hold_note_durations(action_data):
        """
        Takes action_data, filters out non hold notes, and reduces them to
        durations they last for. For example,
        ::
            [138317.,      1.,      0.],
            [138567.,      3.,      0.],
            [138651.,      1.,      1.],
            [138901.,      2.,      2.],
            [138984.,      2.,      2.],
            [139234.,      3.,      3.],

        becomes
        ::
            [138317.,      250.,    0.  ],
            [138567.,      0.,      0.  ],
            [138651.,      583.,    583.],
            [138901.,      0.,      0.  ],
            [138984.,      0.,      0.  ],
            [139234.,      0.,      0.  ],

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        numpy.array
        action_data with hold note durations
        """
        # Make a copy of the data and keep just the timings
        hold_note_duration_data = action_data.copy()
        hold_note_duration_data[:, 1:] = 0

        # Make another copy of the data to have just stuff related to hold notes
        hold_note_mask = ManiaMapMetrics.detect_hold_notes(action_data)
        hold_note_data = action_data.copy()

        # Keep just the information associated with hold notes
        hold_note_data[:, 1:][~hold_note_mask[:, 1:].astype(np.bool, copy=False)] = 0

        # Get idx where presses and releases occur. This is 2D data: (timings, columns)
        where_release = np.where(np.isin(hold_note_data[:, 1:], ManiaActionData.RELEASE))
        where_press   = np.where(np.isin(hold_note_data[:, 1:], ManiaActionData.PRESS))

        # Operate per column (because idk how to make numpy operate on all columns like this)
        for col in range(ManiaActionData.num_keys(action_data)):
            # For current column, get where PRESS and RELEASE occur
            where_release_timing = where_release[0][where_release[1] == col]
            where_press_timing   = where_press[0][where_press[1] == col]

            # Get timings for those PRESS and RELEASE
            release_timings = action_data[where_release_timing][:,0]
            press_timings   = action_data[where_press_timing][:,0]

            # This contains a list of hold note durations. The locations of the hold note durations are
            # resolved via where_press_timing
            hold_note_durations = release_timings - press_timings

            # Now fill in the blank data with hold note durations
            hold_note_duration_data[:, col + 1][where_press_timing] = hold_note_durations
        
        return hold_note_duration_data


    @staticmethod
    def data_to_anti_press_durations(action_data):
        """
        Takes action_data, and reduces them to durations of anti-presses. Anti-presses
        are associated with points in LN type patterns where there is a spot between 
        two holdnotes where the finger is released. For example,
        ::
            [138317.,      1.,      0.],
            [138567.,      3.,      0.],
            [138651.,      1.,      1.],
            [138901.,      2.,      2.],
            [138984.,      2.,      2.],
            [139234.,      3.,      3.],

        becomes
        ::
            [138317.,      0.,      0.  ],
            [138567.,      84.,     0.  ],
            [138651.,      0.,      0.  ],
            [138901.,      0.,      0.  ],
            [138984.,      0.,      0.  ],
            [139234.,      0.,      0.  ],

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        numpy.array
        action_data with hold note durations
        """
        # Make a copy of the data and keep just the timings
        anti_press_duration_data = action_data.copy()
        anti_press_duration_data[:, 1:] = 0

        # Make another copy of the data to have just stuff related to hold notes
        hold_note_mask = ManiaMapMetrics.detect_hold_notes(action_data)
        hold_note_data = action_data.copy()

        # Keep just the information associated with hold notes
        hold_note_data[:, 1:][~hold_note_mask[:, 1:].astype(np.bool, copy=False)] = 0

        # Get idx where presses and releases occur. This is 2D data: (timings, columns)
        where_release = np.where(np.isin(hold_note_data[:, 1:], ManiaActionData.RELEASE))
        where_press   = np.where(np.isin(hold_note_data[:, 1:], ManiaActionData.PRESS))

        # Operate per column (because idk how to make numpy operate on all columns like this)
        for col in range(ManiaActionData.num_keys(action_data)):
            # For current column, get where PRESS and RELEASE occur
            where_release_timing = where_release[0][where_release[1] == col]
            where_press_timing   = where_press[0][where_press[1] == col]

            # Get timings for those PRESS and RELEASE. We drop the last release timing because
            # There is no press after that, hence no anti-press. We drop the first press timing
            # because there is no release before that, hence no anti-press
            release_timings = action_data[where_release_timing][:-1,0]
            press_timings   = action_data[where_press_timing][1:,0]

            # This contains a list of anti-press durations. The locations of the anti-press durations are
            # resolved via where_release_timing
            anti_press_durations = press_timings - release_timings

            # Now fill in the blank data with anti-press durations
            anti_press_duration_data[:, col + 1][where_release_timing[:-1]] = anti_press_durations
        
        return anti_press_duration_data


    @staticmethod
    def detect_holds_during_release(action_data):
        """
        Masks holds that occur when there is at least one release in one of the columns

        This is useful for determining which holds are harder due to finger independence.
        Releases have a tendency to make affected fingers release prematurely.

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        numpy.array
        action_data mask of actions detected
        """
        hold_mask = ManiaActionData.mask_actions(action_data, ManiaActionData.HOLD)

        release_mask_any = np.any(action_data[:, 1:] == ManiaActionData.RELEASE, 1)
        hold_mask_any    = np.any(action_data[:, 1:] == ManiaActionData.HOLD, 1)
        release_and_hold = np.logical_and(release_mask_any, hold_mask_any)

        hold_mask[:, 1:] = release_and_hold[:, None] * hold_mask[:, 1:]
        return hold_mask


    @staticmethod
    def detect_chords(action_data):
        """
        Masks note that are detected as chords

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        numpy.array
        action_data mask of actions detected that correspond to chord patterns. 1 if chord pattern 0 otherwise
        """
        mask = ManiaActionData.mask_actions(action_data, [ ManiaActionData.PRESS ])
        
        '''
        A note is chord if:
            - It is among 3 or more other notes in same action
            - TODO: It is among 3 or more other notes in range of actions within tolerance interval
        '''
        for action in mask:
            presses = action[1:][action[1:] == ManiaActionData.PRESS]
            if len(presses) < 3: action[1:][action[1:] == ManiaActionData.PRESS] = 0

        return mask


    
    @staticmethod
    def detect_jacks(action_data):
        """
        Masks note that are detected as jacks

        Parameters
        ----------
        action_data : numpy.array
            Action data from ``ManiaActionData.get_action_data``

        Returns
        -------
        numpy.array
        action_data mask of actions detected that correspond to jack patterns. 1 if jack pattern 0 otherwise
        """
        mask = np.zeros(action_data.shape)
        mask[:, 0] = action_data[:, 0]

        state = np.zeros(action_data.shape[1] - 1)
        for i in range(1, len(action_data)):
            state = np.logical_and(np.logical_or(action_data[i - 1, 1:], state), np.logical_or(action_data[i, 1:], ~np.any(action_data[i, 1:])))
            mask[i, 1:] = np.logical_and(action_data[i, 1:], state)

        return mask


    @staticmethod
    def calc_note_intervals(hitobject_data, column):
        """
        Gets the duration (time interval) between each note in the specified ``column``

        Parameters
        ----------
        hitobject_data : numpy.array
            Hitobject data from ``ManiaMapData.get_hitobject_data``

        column : int
            Which column number to get note intervals for

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(start_times, intervals)``. ``start_times`` are timings corresponding to start of notes. 
            ``intervals`` are the timings difference between current and previous notes' starting times. 
            Resultant array size is ``len(hitobject_data) - 1``.
        """
        start_times = ManiaMapData.start_times(hitobject_data, column)
        if len(start_times) < 2: return [], []
    
        return start_times[1:], np.diff(start_times)


    @staticmethod
    def calc_notes_per_sec(hitobject_data, column=None):
        """
        Gets average note rate with window of 1 second throughout the beatmap in the specified ``column``

        Parameters
        ----------
        hitobject_data : numpy.array
            Hitobject data from ``ManiaMapData.get_hitobject_data``

        column : int
            Which column number to get average note rate for. If left blank, interprets all columns as one.

        Returns
        -------
        (numpy.array, numpy.array)
            Tuple of ``(start_times, notes_per_sec)``. ``start_times`` are timings corresponding to start of notes. 
            ``notes_per_sec`` are average note rates at ``start_times`` point in time. Resultant array size is 
            ``len(hitobject_data) - 1``.
        """
        if column == None:
            start_times = ManiaMapData.start_times(hitobject_data)
            mask, filtered_start_times, processed_start_times = NumpyUtils.mania_chord_to_jack(start_times)

            if len(start_times) < 2: return [], []
            intervals = 1000/(processed_start_times[1:] - filtered_start_times[:-1])
        
            return start_times[mask == 0][1:], intervals
        else:
            start_times = ManiaMapData.start_times(hitobject_data, column)

            if len(start_times) < 2: return [], []
            intervals = 1000/np.diff(start_times)
        
            return start_times[1:], intervals


    @staticmethod
    def calc_avg_nps_col(hitobject_data, time, ms_window, column):
        """
        Gets average notes with window of ``ms_window`` for the specified ``column`` at time ``time``

        Parameters
        ----------
        hitobject_data : numpy.array
            Hitobject data from ``ManiaMapData.get_hitobject_data``

        time: int
            Time to calculate notes per second for

        ms_window: int
            Milliseconds back in time to take account

        column : int
            Which column number to get average note rate for

        Returns
        -------
        float
            Average notes per second for specified column
        """
        start_times = ManiaMapData.start_times(hitobject_data, column)
        start_times = start_times[time - ms_window <= start_times <= time]
        intervals   = np.diff(start_times)/1000
        return np.mean(intervals)


    @staticmethod
    def calc_avg_nps(hitobject_data, time, ms_window):
        """
        Gets average notes with window of ``ms_window`` for all columns at time ``time``

        Parameters
        ----------
        hitobject_data : numpy.array
            Hitobject data from ``ManiaMapData.get_hitobject_data``

        time: int
            Time to calculate notes per second for

        ms_window: int
            Milliseconds back in time to take account

        Returns
        -------
        float
            Average notes per second
        """
        avg_nps = np.asarray([ ManiaMapMetrics.calc_avg_nps_col(hitobject_data, time, ms_window, column) for column in len(hitobject_data) ])
        return np.mean(avg_nps)


    @staticmethod
    def to_binary_signal(hitobject_data, tap_duration=25):
        """
        Returns a binary signal indicating press or release for the specified 
        column at the ms resolution specified

        tap_duration: Length of a single tap
        """
        end_time = ManiaMapData.end_times(hitobject_data)[-1]
        signals = np.zeros((len(hitobject_data), end_time))

        for column in range(len(hitobject_data)):
            for x,y in ManiaMapData.start_end_times(hitobject_data, column):
                if x == y: y += tap_duration
                signals[column][x:y] = 1

        return np.arange(end_time), signals


    @staticmethod
    def hand_hold(hitobject_data, min_release=150):
        """
        Dermines on a scale from 0.0 to 1.0 how likely a player can't raise their hand
        Returns two values, for left and right hand

        time: time to calculate notes per second for
        ms_window: how many ms back in time to take account
        """
        time, signals = ManiaMapMetrics.to_binary_signal(hitobject_data, tap_duration=25)
        kernel  = np.ones(min_release)
        conv    = np.apply_along_axis(lambda data: np.convolve(data, kernel, mode='same'), axis=1, arr=signals)
        
        # TODO: kernel_left, kernel_right; size: int(len(conv)/2)
        kernel = [[1], 
                  [1]]
          
        # Valid because we need to conv multiple columns into one array indicating whether hand will be held down
        conv_left = signal.convolve2d(conv[:int(len(conv)/2)], kernel, 'valid')
        conv_left = np.clip(conv_left, 0, 1)

        conv_right = signal.convolve2d(conv[int(len(conv)/2):], kernel, 'valid')
        conv_right = np.clip(conv_right, 0, 1)
        
        return time, conv_left[0], conv_right[0]


    @staticmethod
    def hand_hold_ratio(hitobject_data, min_release=150):
        time, hand_hold_left, hand_hold_right = ManiaMapMetrics.hand_hold(hitobject_data, min_release)
        left_ratio  = sum(hand_hold_left)/len(hand_hold_left)
        right_ratio = sum(hand_hold_right)/len(hand_hold_right)

        return left_ratio, right_ratio
       