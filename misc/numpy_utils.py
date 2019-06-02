import itertools
import numpy as np


class NumpyUtils():            

    @staticmethod
    def dists(x_list, y_list):
        if len(x_list) < 1 or len(y_list) < 1: return np.array([])
        return np.sqrt((x_list[:,0] - y_list[:,0])**2 + (x_list[:,1] - y_list[:,1])**2)


    @staticmethod
    def func(func, lst):
        return [ func(param) for param in zip(*lst) ]


    @staticmethod
    def first(lst):
        # handle empty array
        n = lst.shape[0]
        if n == 0: return np.array([])

        try: return lst[0]
        except: return None

    
    @staticmethod
    def last(lst):
        # handle empty array
        n = lst.shape[0]
        if n == 0: return np.array([])

        try: return lst[-1]
        except: return None


    # Thanks https://gist.github.com/alimanfoo/c5977e87111abe8127453b21204c1065
    @staticmethod
    def find_runs(lst):
        """
        Info: Find runs of consecutive items in an array.
        Example:
            [in]:  [ 110, 110, 130, 140, 140, 140, 170, 200, 211, 211, 211, 211, 216, 417 ]
            [out]: [ 2, 1, 3, 1, 1, 4, 1, 1 ]
        """

        # ensure array
        lst = np.asanyarray(lst)
        if lst.ndim != 1: raise ValueError('only 1D array supported')

        # handle empty array
        n = lst.shape[0]
        if n == 0: return np.array([])

        else:
            # find run starts
            loc_run_start    = np.empty(n, dtype=bool)
            loc_run_start[0] = True

            np.not_equal(lst[:-1], lst[1:], out=loc_run_start[1:])
            run_starts = np.nonzero(loc_run_start)[0]

            # find run lengths
            run_lengths = np.diff(np.append(run_starts, n))

        return run_lengths


    @staticmethod
    def mania_chord_to_jack(lst):
        """
        Used for notes/second calculation. Converts chords to jack equivalent based on note timings.
        So, for example, 2 note chords 1 second apart can be interpreted as single note jacks 500ms apart
        3 note chords 1 second apart can be interepreted as sing note jacks 333.33ms apart, and so on.
        """

        # When the input_array is diffed, unchanging sequences will be 0. We can detect
        # which indices that occurs at using np.where. Since the indices will correspond to
        # the first value of the unchanging sequence, we need to add by 1 to get every
        # same value but the first one
        idx_diff = np.where(np.diff(lst) == 0)[0] + 1

        # The mask for unchanging values in input_array
        mask           = np.zeros(len(lst))
        mask[idx_diff] = 1

        # Filter out repetitions
        filtered = lst[mask == 0]

        # Get values corresponding to how many consecutive value in a row there are
        mult = 1/NumpyUtils.find_runs(lst)

        # Delta between values; append 0 at beginning since the operation truncated the start
        diff = np.insert(np.diff(filtered), 0, 0)

        # output = curr_val - (curr_val - prev_val)/num_consecutive
        return mask, filtered, filtered - diff*(1-mult)