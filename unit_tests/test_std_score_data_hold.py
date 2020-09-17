import unittest
import pandas as pd

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.replay.replayIO import ReplayIO

from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.replay_data import StdReplayData
from analysis.osu.std.score_data import StdScoreData



class TestStdScoreDataHold(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        map_data = [ 
            pd.DataFrame(
            [
                [ 100, 0,   0, StdMapData.TYPE_PRESS, StdMapData.TYPE_SLIDER ],
                [ 350, 100, 0, StdMapData.TYPE_HOLD, StdMapData.TYPE_SLIDER ],
                [ 600, 200, 0, StdMapData.TYPE_HOLD, StdMapData.TYPE_SLIDER ],
                [ 750, 300, 0, StdMapData.TYPE_RELEASE, StdMapData.TYPE_SLIDER ],
            ],
            columns=['time', 'x', 'y', 'type', 'object']),
            pd.DataFrame(
            [ 
                [ 1000, 500, 500, StdMapData.TYPE_PRESS, StdMapData.TYPE_CIRCLE ],
                [ 1001, 500, 500, StdMapData.TYPE_RELEASE, StdMapData.TYPE_CIRCLE ],
            ],
            columns=['time', 'x', 'y', 'type', 'object']),
            pd.DataFrame(
            [ 
                [ 2000, 300, 300, StdMapData.TYPE_PRESS, StdMapData.TYPE_CIRCLE ],
                [ 2001, 300, 300, StdMapData.TYPE_RELEASE, StdMapData.TYPE_CIRCLE ],
            ],
            columns=['time', 'x', 'y', 'type', 'object']),
        ]
        cls.map_data = pd.concat(map_data, axis=0, keys=range(len(map_data)), names=[ 'hitobject', 'aimpoint' ])

        # Set hitwindow ranges to what these tests have been written for
        StdScoreData.pos_hit_range      = 300    # ms point of late hit window
        StdScoreData.neg_hit_range      = 300    # ms point of early hit window
        StdScoreData.pos_hit_miss_range = 450    # ms point of late miss window
        StdScoreData.neg_hit_miss_range = 450    # ms point of early miss window
    
        StdScoreData.pos_rel_range       = 500   # ms point of late release window
        StdScoreData.neg_rel_range       = 500   # ms point of early release window
        StdScoreData.pos_rel_miss_range  = 1000  # ms point of late release window
        StdScoreData.neg_rel_miss_range  = 1000  # ms point of early release window

        StdScoreData.neg_hld_range       = 50    # ms range of early hold
        StdScoreData.pos_hld_range       = 1000  # ms range of late hold


    @classmethod
    def tearDown(cls):  
        pass


    def test_slider_start_hold_misaim__window_miss(self):
        StdScoreData.hold_range_window = True
        StdScoreData.hold_range_miss   = True

        # Time:     0 ms -> 3000 ms
        # Location: Blank area (1000, 1000)
        # Scoring:  Awaiting press at slider start (100 ms @ (0, 0))
        # Behavior:
        #   Scorepoint awaits PRESS -> NOP
        #   -> NOP
        for ms in range(0, 3000):
            score_data = {}
            adv = StdScoreData._StdScoreData__process_hold(score_data, self.map_data, ms, 1000, 1000)
            
            offset = ms - self.map_data.iloc[0]['time']

            self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
            self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')


    def test_slider_start_hold_nomisaim__window_miss(self):
        StdScoreData.hold_range_window = True
        StdScoreData.hold_range_miss   = True

        # Time:     0 ms -> 3000 ms
        # Location: Blank area (1000, 1000)
        # Scoring:  Awaiting press at slider start (100 ms @ (0, 0))
        # Behavior:
        #   Scorepoint awaits PRESS -> NOP
        #   -> NOP
        for ms in range(0, 3000):
            score_data = {}
            adv = StdScoreData._StdScoreData__process_hold(score_data, self.map_data, ms, 1000, 1000)
            
            offset = ms - self.map_data.iloc[0]['time']

            self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
            self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')


    def test_slider_aimpoint_hold_misaim__window_miss(self):
        StdScoreData.hold_range_window = True
        StdScoreData.hold_range_miss   = True

        # Time:     0 ms -> 3000 ms
        # Location: Blank area (1000, 1000)
        # Scoring:  Awaiting hold at slider aimpoint (350 ms @ (100, 0))
        # Behavior:
        #   Scorepoint awaits HOLD -> ok
        #   Cursor is NOT within press scorepoint range | window & miss -> MISS
        #   -> MISS
        for ms in range(0, 3000):
            score_data = {}
            adv = StdScoreData._StdScoreData__process_hold(score_data, self.map_data.iloc[1:], ms, 1000, 1000)
            
            offset = ms - self.map_data.iloc[1]['time']

            self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOTE, f'Offset: {offset} ms')
            self.assertEqual(score_data[0][6], StdScoreData.TYPE_MISS, f'Offset: {offset} ms')


    def test_slider_aimpoint_hold_misaim__window_nomiss(self):
        StdScoreData.hold_range_window = True
        StdScoreData.hold_range_miss   = False

        # Time:     0 ms -> 3000 ms
        # Location: Blank area (1000, 1000)
        # Scoring:  Awaiting hold at slider aimpoint (350 ms @ (100, 0))
        # Behavior:
        #   Scorepoint awaits HOLD -> ok
        #   Cursor is NOT within press scorepoint range | window -> NOP
        #   -> NOP
        for ms in range(0, 3000):
            score_data = {}
            adv = StdScoreData._StdScoreData__process_hold(score_data, self.map_data.iloc[1:], ms, 1000, 1000)
            
            offset = ms - self.map_data.iloc[1]['time']

            self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
            self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')


    def test_slider_aimpoint_hold_misaim__nowindow_miss(self):
        StdScoreData.hold_range_window = False
        StdScoreData.hold_range_miss   = True

        # Time:     0 ms -> 3000 ms
        # Location: Blank area (1000, 1000)
        # Scoring:  Awaiting hold at slider aimpoint (350 ms @ (100, 0))
        # Behavior:
        #   Scorepoint awaits HOLD -> ok
        #   Cursor is NOT within press scorepoint range -> NOP
        #   -> NOP
        for ms in range(0, 3000):
            score_data = {}
            adv = StdScoreData._StdScoreData__process_hold(score_data, self.map_data.iloc[1:], ms, 1000, 1000)
            
            offset = ms - self.map_data.iloc[1]['time']

            if offset <= -StdScoreData.neg_hld_range:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
                self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')

            if -StdScoreData.neg_hld_range < offset <= StdScoreData.pos_hld_range:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_AIMP, f'Offset: {offset} ms')
                self.assertEqual(score_data[0][6], StdScoreData.TYPE_AIMH, f'Offset: {offset} ms')

            if StdScoreData.pos_hld_range < offset:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
                self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')


    def test_slider_aimpoint_hold_nomisaim__window_miss(self):
        StdScoreData.hold_range_window = True
        StdScoreData.hold_range_miss   = True

        # Time:     0 ms -> 3000 ms
        # Location: At slider aimpoint (100, 0)
        # Scoring:  Awaiting hold at slider aimpoint (350 ms @ (100, 0))
        # Behavior:
        #   Scorepoint awaits HOLD -> ok
        #   Cursor is within press scorepoint range -> ok
        #   Within hold range  -> AIMH
        #   Outside hold range -> NOP
        for ms in range(0, 3000):
            score_data = {}
            adv = StdScoreData._StdScoreData__process_hold(score_data, self.map_data.iloc[1:], ms, 100, 0)
            
            offset = ms - self.map_data.iloc[1]['time']

            if offset <= -StdScoreData.neg_hld_range:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
                self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')

            if -StdScoreData.neg_hld_range < offset <= StdScoreData.pos_hld_range:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_AIMP, f'Offset: {offset} ms')
                self.assertEqual(score_data[0][6], StdScoreData.TYPE_AIMH, f'Offset: {offset} ms')

            if StdScoreData.pos_hld_range < offset:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
                self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')


    def test_slider_aimpoint_hold_nomisaim__nowindow_nomiss(self):
        StdScoreData.hold_range_window = False
        StdScoreData.hold_range_miss   = False

        # Time:     0 ms -> 3000 ms
        # Location: At slider aimpoint (100, 0)
        # Scoring:  Awaiting hold at slider aimpoint (350 ms @ (100, 0))
        for ms in range(0, 3000):
            score_data = {}
            adv = StdScoreData._StdScoreData__process_hold(score_data, self.map_data.iloc[1:], ms, 100, 0)
            
            offset = ms - self.map_data.iloc[1]['time']

            if offset <= -StdScoreData.neg_hld_range:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
                self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')

            if -StdScoreData.neg_hld_range < offset <= StdScoreData.pos_hld_range:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_AIMP, f'Offset: {offset} ms')
                self.assertEqual(score_data[0][6], StdScoreData.TYPE_AIMH, f'Offset: {offset} ms')

            if StdScoreData.pos_hld_range < offset:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
                self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')


    def test_slider_aimpoint_hold_nomisaim__nowindow_miss(self):
        StdScoreData.hold_range_window = False
        StdScoreData.hold_range_miss   = True

        # Time:     0 ms -> 3000 ms
        # Location: At slider aimpoint (100, 0)
        # Scoring:  Awaiting hold at slider aimpoint (350 ms @ (100, 0))
        for ms in range(0, 3000):
            score_data = {}
            adv = StdScoreData._StdScoreData__process_hold(score_data, self.map_data.iloc[1:], ms, 100, 0)
            
            offset = ms - self.map_data.iloc[1]['time']

            if offset <= -StdScoreData.neg_hld_range:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
                self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')

            if -StdScoreData.neg_hld_range < offset <= StdScoreData.pos_hld_range:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_AIMP, f'Offset: {offset} ms')
                self.assertEqual(score_data[0][6], StdScoreData.TYPE_AIMH, f'Offset: {offset} ms')

            if StdScoreData.pos_hld_range < offset:
                self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
                self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')


    def test_slider_release_hold_nomisaim__window_miss(self):
        StdScoreData.hold_range_window = True
        StdScoreData.hold_range_miss   = True

        # Time:     0 ms -> 3000 ms
        # Location: At slider release (300, 0)
        # Scoring:  Awaiting release at slider end (750 ms @ (300, 0))
        for ms in range(0, 3000):
            score_data = {}
            adv = StdScoreData._StdScoreData__process_hold(score_data, self.map_data.iloc[3:], ms, 300, 0)
            
            offset = ms - self.map_data.iloc[3]['time']

            self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
            self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')


    def test_circle_hold_nomisaim__window_miss(self):
        StdScoreData.hold_range_window = True
        StdScoreData.hold_range_miss   = True

        # Time:     0 ms -> 3000 ms
        # Location: At 1st hitcircle (500, 500)
        # Scoring:  Awaiting press at 1st hitcircle (1000 ms @ (500, 500))
        for ms in range(0, 3000):
            score_data = {}
            adv = StdScoreData._StdScoreData__process_hold(score_data, self.map_data.iloc[4:], ms, 500, 500)
            
            offset = ms - self.map_data.iloc[4]['time']

            self.assertEqual(adv, StdScoreData._StdScoreData__ADV_NOP, f'Offset: {offset} ms')
            self.assertEqual(len(score_data), 0, f'Offset: {offset} ms')