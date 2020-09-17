import unittest
import pandas as pd

from osu.local.beatmap.beatmapIO import BeatmapIO
from analysis.osu.std.map_data import StdMapData



class TestStdMapData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\test\\abraker - unknown (abraker) [250ms].osu')
       
        map_data = [ 
            pd.DataFrame(
            [
                [ 100, 0, 0, StdMapData.TYPE_PRESS, StdMapData.TYPE_SLIDER ],
                [ 200, 0, 0, StdMapData.TYPE_HOLD, StdMapData.TYPE_SLIDER ],
                [ 300, 0, 0, StdMapData.TYPE_HOLD, StdMapData.TYPE_SLIDER ],
                [ 400, 0, 0, StdMapData.TYPE_RELEASE, StdMapData.TYPE_SLIDER ],
            ],
            columns=['time', 'x', 'y', 'type', 'object']),
            pd.DataFrame(
            [ 
                [ 1100, 0, 0, StdMapData.TYPE_PRESS, StdMapData.TYPE_CIRCLE ],
                [ 1101, 0, 0, StdMapData.TYPE_RELEASE, StdMapData.TYPE_CIRCLE ],
            ],
            columns=['time', 'x', 'y', 'type', 'object']),
            pd.DataFrame(
            [ 
                [ 2100, 0, 0, StdMapData.TYPE_PRESS, StdMapData.TYPE_CIRCLE ],
                [ 2101, 0, 0, StdMapData.TYPE_RELEASE, StdMapData.TYPE_CIRCLE ],
            ],
            columns=['time', 'x', 'y', 'type', 'object']),
        ]
        cls.map_data = pd.concat(map_data, axis=0, keys=range(len(map_data)), names=[ 'hitobject', 'aimpoint' ])


    @classmethod
    def tearDown(cls):  
        pass


    def test_std_hitobject_to_aimpoints(self):
        for hitobject in self.beatmap.hitobjects:
            aimpoint_data = StdMapData.std_hitobject_to_aimpoints(hitobject)


    def test_get_map_data(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)


    def test_get_num_hitobjects(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        num_hitobjects = StdMapData.get_num_hitobjects(map_data)


    def test_get_presses(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        presses = StdMapData.get_presses(map_data)


    def test_get_releases(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        presses = StdMapData.get_releases(map_data)


    def test_get_scorepoint_before(self):
        # Time: Before start
        scorepoint_data = StdMapData.get_scorepoint_before(self.map_data, 0)
        self.assertEqual(scorepoint_data, None)

        # Time: At first aimpoint
        scorepoint_data = StdMapData.get_scorepoint_before(self.map_data, 100)
        self.assertEqual(scorepoint_data, None)

        # Time: At second aimpoint
        scorepoint_data = StdMapData.get_scorepoint_before(self.map_data, 200)
        self.assertEqual(scorepoint_data['time'], 100)

        # Time: At slider release
        scorepoint_data = StdMapData.get_scorepoint_before(self.map_data, 400)
        self.assertEqual(scorepoint_data['time'], 300)

        # Time: At 2nd hitobject
        scorepoint_data = StdMapData.get_scorepoint_before(self.map_data, 1100)
        self.assertEqual(scorepoint_data['time'], 400)

        # Time: At last hitobject
        scorepoint_data = StdMapData.get_scorepoint_before(self.map_data, 2100)
        self.assertEqual(scorepoint_data['time'], 1101)

        # Time: After last hitobject
        scorepoint_data = StdMapData.get_scorepoint_before(self.map_data, 2200)
        self.assertEqual(scorepoint_data['time'], 2101)


    def test_get_scorepoint_after(self):
        # Time: Before start
        scorepoint_data = StdMapData.get_scorepoint_after(self.map_data, 0)
        self.assertEqual(scorepoint_data['time'], 100)

        # Time: At first aimpoint
        scorepoint_data = StdMapData.get_scorepoint_after(self.map_data, 100)
        self.assertEqual(scorepoint_data['time'], 200)

        # Time: At second aimpoint
        scorepoint_data = StdMapData.get_scorepoint_after(self.map_data, 200)
        self.assertEqual(scorepoint_data['time'], 300)

        # Time: At slider release
        scorepoint_data = StdMapData.get_scorepoint_after(self.map_data, 400)
        self.assertEqual(scorepoint_data['time'], 1100)

        # Time: At 2nd hitobject
        scorepoint_data = StdMapData.get_scorepoint_after(self.map_data, 1100)
        self.assertEqual(scorepoint_data['time'], 1101)

        # Time: At last hitobject
        scorepoint_data = StdMapData.get_scorepoint_after(self.map_data, 2100)
        self.assertEqual(scorepoint_data['time'], 2101)

        # Time: After last hitobject
        scorepoint_data = StdMapData.get_scorepoint_after(self.map_data, 2200)
        self.assertEqual(scorepoint_data, None)
        

    '''
    def test_get_next_hitobject_idx(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\playable\\Within Temptation - The Unforgiving (Armin) [Marathon].osu')
        map_data = StdMapData.get_map_data(beatmap.hitobjects)

        idx = -1
        while idx != None:
            idx = StdMapData.get_next_hitobject_idx(map_data, idx)
    '''


    def test_get_visible_at(self):
        for time in range(-1000, 10000, 100):
            visible = StdMapData.get_visible_at(self.map_data, time, 400)


    def test_get_note_before(self):
        # Time: Before start
        hitobject_data = StdMapData.get_note_before(self.map_data, 0)
        self.assertEqual(hitobject_data, None)

        # Time: At first aimpoint
        hitobject_data = StdMapData.get_note_before(self.map_data, 100)
        self.assertEqual(hitobject_data, None)

        # Time: At second aimpoint
        hitobject_data = StdMapData.get_note_before(self.map_data, 200)
        self.assertEqual(hitobject_data.iloc[0]['time'], 100)

        # Time: At slider release
        hitobject_data = StdMapData.get_note_before(self.map_data, 400)
        self.assertEqual(hitobject_data.iloc[0]['time'], 100)

        # Time: At 2nd hitobject
        hitobject_data = StdMapData.get_note_before(self.map_data, 1100)
        self.assertEqual(hitobject_data.iloc[0]['time'], 100)

        # Time: At last hitobject
        hitobject_data = StdMapData.get_note_before(self.map_data, 2100)
        self.assertEqual(hitobject_data.iloc[0]['time'], 1100)

        # Time: After last hitobject
        hitobject_data = StdMapData.get_note_before(self.map_data, 2101)
        self.assertEqual(hitobject_data.iloc[0]['time'], 2100)


    def test_get_note_after(self):
        # Time: Before start
        hitobject_data = StdMapData.get_note_after(self.map_data, 0)
        self.assertEqual(hitobject_data.iloc[0]['time'], 100)

        # Time: At first aimpoint
        hitobject_data = StdMapData.get_note_after(self.map_data, 100)
        self.assertEqual(hitobject_data.iloc[0]['time'], 1100)

        # Time: At second aimpoint
        hitobject_data = StdMapData.get_note_after(self.map_data, 200)
        self.assertEqual(hitobject_data.iloc[0]['time'], 1100)

        # Time: At slider release
        hitobject_data = StdMapData.get_note_after(self.map_data, 400)
        self.assertEqual(hitobject_data.iloc[0]['time'], 1100)

        # Time: At 2nd hitobject
        hitobject_data = StdMapData.get_note_after(self.map_data, 1100)
        self.assertEqual(hitobject_data.iloc[0]['time'], 2100)

        # Time: At last hitobject
        hitobject_data = StdMapData.get_note_after(self.map_data, 2100)
        self.assertEqual(hitobject_data, None)

        # Time: After last hitobject
        hitobject_data = StdMapData.get_note_after(self.map_data, 2101)
        self.assertEqual(hitobject_data, None)


    def test_time_slice(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        map_data = StdMapData.time_slice(map_data, 1000, 2000, True)

        self.assertGreaterEqual(map_data['time'].values[0], 1000)
        self.assertLessEqual(map_data['time'].values[0], 2000)


    def test_start_times(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        start_times = StdMapData.start_times(map_data)


    def test_end_times(self):
        map_data = StdMapData.get_map_data(self.beatmap.hitobjects)
        end_times = StdMapData.end_times(map_data)