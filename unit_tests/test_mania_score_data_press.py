import unittest
import pandas as pd

from analysis.osu.mania.action_data import ManiaActionData
from analysis.osu.mania.score_data import ManiaScoreData



class TestManiaScoreDataPress(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        action_data = {
             50 : [ 0, 0, 0, 1 ],
             51 : [ 0, 0, 0, 3 ],
            100 : [ 0, 0, 0, 1 ],
            101 : [ 0, 0, 0, 3 ],
            150 : [ 0, 0, 0, 1 ],
            200 : [ 0, 0, 0, 2 ],
            250 : [ 0, 0, 0, 3 ],
            300 : [ 1, 0, 0, 1 ],
            301 : [ 3, 0, 0, 2 ],
            350 : [ 0, 0, 0, 3 ],
            400 : [ 0, 0, 0, 0 ],
            450 : [ 1, 1, 1, 1 ],
            451 : [ 3, 2, 3, 3 ],
            500 : [ 0, 3, 0, 0 ],
        }
        
        # Sort data by timings
        action_data = dict(sorted(action_data.items()))

        # Convert the dictionary of recorded timings and states into a pandas data
        cls.map_data = pd.DataFrame.from_dict(action_data, orient='index')
        cls.map_data.index.name = 'time'

        cls.map_col = cls.map_data[3][cls.map_data[3] != ManiaActionData.FREE].values
        cls.map_times = cls.map_data.index[cls.map_data[3] != ManiaActionData.FREE].values

        # Set hitwindow ranges to what these tests have been written for
        ManiaScoreData.pos_hit_range       = 100  # ms point of late hit window
        ManiaScoreData.neg_hit_range       = 100  # ms point of early hit window
        ManiaScoreData.pos_hit_miss_range  = 150  # ms point of late miss window
        ManiaScoreData.neg_hit_miss_range  = 150  # ms point of early miss window
    
        ManiaScoreData.pos_rel_range       = 100  # ms point of late release window
        ManiaScoreData.neg_rel_range       = 100  # ms point of early release window
        ManiaScoreData.pos_rel_miss_range  = 150  # ms point of late release window
        ManiaScoreData.neg_rel_miss_range  = 150  # ms point of early release window


    @classmethod
    def tearDown(cls):  
        pass


    def test_no_press__singlenote_press__noblank_nolazy(self):
        # Time:     -1000 ms -> 1000 ms
        # Scoring:  Awaiting press at first singlenote (50 ms @ (col 3))
        ManiaScoreData.blank_miss = False
        ManiaScoreData.lazy_sliders = False

        map_idx = 0
        scorepoint_type = self.map_col[map_idx]

        self.assertEqual(scorepoint_type, ManiaActionData.PRESS)

        for ms in range(-1000, 1000):
            column_data = {}
            offset = ms - self.map_times[map_idx]
            adv = ManiaScoreData._ManiaScoreData__process_free(column_data, scorepoint_type, ms, self.map_times, map_idx)
            
            if offset <= ManiaScoreData.pos_hit_miss_range:
                self.assertEqual(adv, 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
            else:
                self.assertEqual(adv, 2, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_MISS, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')


    def test_press__singlenote_press__noblank_nolazy(self):
        # Time:     -1000 ms -> 1000 ms
        # Scoring:  Awaiting press at first singlenote (50 ms @ (col 3))
        ManiaScoreData.blank_miss = False
        ManiaScoreData.lazy_sliders = False
        
        map_idx = 0
        scorepoint_type = self.map_col[map_idx]

        self.assertEqual(scorepoint_type, ManiaActionData.PRESS)

        for ms in range(-1000, 1000):
            column_data = {}
            offset = ms - self.map_times[map_idx]
            adv = ManiaScoreData._ManiaScoreData__process_press(column_data, ms, self.map_times, map_idx)

            if offset <= -ManiaScoreData.neg_hit_miss_range:
                self.assertEqual(adv, 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
            
            elif -ManiaScoreData.neg_hit_miss_range < offset <= -ManiaScoreData.neg_hit_range:
                self.assertEqual(adv, 2, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_MISS, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            elif -ManiaScoreData.neg_hit_range < offset <= ManiaScoreData.pos_hit_range:
                self.assertEqual(adv, 2, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_HITP, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            elif ManiaScoreData.pos_hit_range < offset <= ManiaScoreData.pos_hit_miss_range:
                self.assertEqual(adv, 2, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_MISS, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            elif ManiaScoreData.pos_hit_miss_range < offset:
                self.assertEqual(adv, 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            else:
                self.fail(f'Unexpected condition |  Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')


    def test_free__singlenote_release__noblank_nolazy(self):
        # Time:     -1000 ms -> 1000 ms
        # Scoring:  Awaiting release at first singlenote (100 ms @ (col 3))
        ManiaScoreData.blank_miss = False
        ManiaScoreData.lazy_sliders = False

        map_idx = 1
        scorepoint_type = self.map_col[map_idx]

        self.assertEqual(scorepoint_type, ManiaActionData.RELEASE)

        for ms in range(-1000, 1000):
            column_data = {}
            offset = ms - self.map_times[map_idx]
            adv = ManiaScoreData._ManiaScoreData__process_free(column_data, scorepoint_type, ms, self.map_times, map_idx)

            if offset <= ManiaScoreData.pos_hit_miss_range:
                self.assertEqual(adv, 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
            else:
                self.assertEqual(adv, 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
            
            self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')


    def test_release__singlenote_release__noblank_nolazy(self):
        # Time:     -1000 ms -> 1000 ms
        # Scoring:  Awaiting release at first singlenote (100 ms @ (col 3))
        ManiaScoreData.blank_miss = False
        ManiaScoreData.lazy_sliders = False

        map_idx = 1
        scorepoint_type = self.map_col[map_idx]

        self.assertEqual(scorepoint_type, ManiaActionData.RELEASE)

        for ms in range(-1000, 1000):
            column_data = {}
            offset = ms - self.map_times[map_idx]
            adv = ManiaScoreData._ManiaScoreData__process_release(column_data, ms, self.map_times, map_idx)

            self.assertEqual(adv, 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
            self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')


    def test_free__holdnote_press__noblank_nolazy(self):
        # Time:     -1000 ms -> 1000 ms
        # Scoring:  Awaiting press at first singlenote (150 ms @ (col 3))
        ManiaScoreData.blank_miss = False
        ManiaScoreData.lazy_sliders = False

        map_idx = 4
        scorepoint_type = self.map_col[map_idx]

        self.assertEqual(scorepoint_type, ManiaActionData.PRESS)

        for ms in range(-1000, 1000):
            column_data = {}
            offset = ms - self.map_times[map_idx]
            adv = ManiaScoreData._ManiaScoreData__process_free(column_data, scorepoint_type, ms, self.map_times, map_idx)
            
            if offset <= ManiaScoreData.pos_hit_miss_range:
                self.assertEqual(adv, 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
            else:
                self.assertEqual(adv, 2, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_MISS, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

        
    def test_press__holdnote_press__noblank_nolazy(self):
        # Time:     -1000 ms -> 1000 ms
        # Scoring:  Awaiting press at first singlenote (150 ms @ (col 3))
        ManiaScoreData.blank_miss = False
        ManiaScoreData.lazy_sliders = False
        
        map_idx = 4
        scorepoint_type = self.map_col[map_idx]

        self.assertEqual(scorepoint_type, ManiaActionData.PRESS)

        for ms in range(-1000, 1000):
            column_data = {}
            offset = ms - self.map_times[map_idx]
            adv = ManiaScoreData._ManiaScoreData__process_press(column_data, ms, self.map_times, map_idx)

            if offset <= -ManiaScoreData.neg_hit_miss_range:
                self.assertEqual(adv, 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
            
            elif -ManiaScoreData.neg_hit_miss_range < offset <= -ManiaScoreData.neg_hit_range:
                self.assertEqual(adv, 2, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_MISS, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            elif -ManiaScoreData.neg_hit_range < offset <= ManiaScoreData.pos_hit_range:
                self.assertEqual(adv, 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_HITP, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            elif ManiaScoreData.pos_hit_range < offset <= ManiaScoreData.pos_hit_miss_range:
                self.assertEqual(adv, 2, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_MISS, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            elif ManiaScoreData.pos_hit_miss_range < offset:
                self.assertEqual(adv, 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            else:
                self.fail(f'Unexpected condition |  Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

    
    def test_release__holdnote_release__noblank_nolazy(self):
        # Time:     -1000 ms -> 1000 ms
        # Scoring:  Awaiting release at first singlenote (250 ms @ (col 3))
        ManiaScoreData.blank_miss = False
        ManiaScoreData.lazy_sliders = False
        
        map_idx = 6
        scorepoint_type = self.map_col[map_idx]

        self.assertEqual(scorepoint_type, ManiaActionData.RELEASE)

        for ms in range(-1000, 1000):
            column_data = {}
            offset = ms - self.map_times[map_idx]
            adv = ManiaScoreData._ManiaScoreData__process_release(column_data, ms, self.map_times, map_idx)

            if offset <= -ManiaScoreData.neg_rel_miss_range:
                self.assertEqual(adv, 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
            
            elif -ManiaScoreData.neg_rel_miss_range < offset <= -ManiaScoreData.neg_rel_range:
                self.assertEqual(adv, 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_MISS, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            elif -ManiaScoreData.neg_rel_range < offset <= ManiaScoreData.pos_rel_range:
                self.assertEqual(adv, 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_HITR, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            elif ManiaScoreData.pos_rel_range < offset <= ManiaScoreData.pos_rel_miss_range:
                self.assertEqual(adv, 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertIn(0, column_data, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

                self.assertEqual(column_data[0][0], ms, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][1], self.map_times[map_idx], f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][2], ManiaScoreData.TYPE_MISS, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(column_data[0][3], map_idx, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            elif ManiaScoreData.pos_rel_miss_range < offset:
                self.assertEqual(adv, 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
                self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')

            else:
                self.fail(f'Unexpected condition |  Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')


    def test_release__holdnote_release__noblank_lazy(self):
        # Time:     -1000 ms -> 1000 ms
        # Scoring:  Awaiting release at first singlenote (250 ms @ (col 3))
        ManiaScoreData.blank_miss = False
        ManiaScoreData.lazy_sliders = True
        
        map_idx = 6
        scorepoint_type = self.map_col[map_idx]

        self.assertEqual(scorepoint_type, ManiaActionData.RELEASE)

        for ms in range(-1000, 1000):
            column_data = {}
            offset = ms - self.map_times[map_idx]
            adv = ManiaScoreData._ManiaScoreData__process_release(column_data, ms, self.map_times, map_idx)

            self.assertEqual(adv, 1, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
            self.assertEqual(len(column_data), 0, f'Offset: {offset} ms;   Replay: {ms} ms;   Map: {self.map_times[map_idx]} ms')
        