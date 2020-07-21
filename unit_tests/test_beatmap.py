import unittest

from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.hitobject.std.std import Std


class TestBeatmap(unittest.TestCase):

    def test_beatmap_loading_mania(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\mania\\playable\\Camellia - GHOST (qqqant) [Collab PHANTASM [MX]].osu')
        
        # Test metadata
        self.assertEqual(beatmap.metadata.beatmap_format, 14)
        self.assertEqual(beatmap.metadata.title, 'GHOST')
        self.assertEqual(beatmap.metadata.artist, 'Camellia')
        self.assertEqual(beatmap.metadata.version, 'Collab PHANTASM [MX]')
        self.assertEqual(beatmap.metadata.creator, 'qqqant')

        # Test timing points
        self.assertEqual(len(beatmap.timing_points), 179)

        self.assertEqual(beatmap.timing_points[0].offset, 8527)
        self.assertEqual(beatmap.timing_points[0].beat_interval, 272.727272727273)
        self.assertEqual(beatmap.timing_points[0].meter, 4)
        self.assertEqual(beatmap.timing_points[0].inherited, False)

        self.assertEqual(beatmap.timing_points[178].offset, 316163)
        self.assertEqual(beatmap.timing_points[178].beat_interval, -125)
        self.assertEqual(beatmap.timing_points[178].meter, 4)
        self.assertEqual(beatmap.timing_points[178].inherited, True)

        # Test hitobjects
        self.assertEqual(len(beatmap.hitobjects), 4)
        self.assertEqual(sum(len(column) for column in beatmap.hitobjects), 3004)

        # TODO: test hitobjects


    def test_beatmap_loading_std(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\playable\\Mutsuhiko Izumi - Red Goose (nold_1702) [ERT Basic].osu')
        
        # Test metadata
        self.assertEqual(beatmap.metadata.beatmap_format, 9)
        self.assertEqual(beatmap.metadata.title, 'Red Goose')
        self.assertEqual(beatmap.metadata.artist, 'Mutsuhiko Izumi')
        self.assertEqual(beatmap.metadata.version, 'ERT Basic')
        self.assertEqual(beatmap.metadata.creator, 'nold_1702')

        # Test timing points
        self.assertEqual(len(beatmap.timing_points), 23)

        self.assertEqual(beatmap.timing_points[0].offset, -401)
        self.assertEqual(beatmap.timing_points[0].beat_interval, 300)
        self.assertEqual(beatmap.timing_points[0].meter, 4)
        self.assertEqual(beatmap.timing_points[0].inherited, False)


        self.assertEqual(beatmap.timing_points[22].offset, 117799)
        self.assertEqual(beatmap.timing_points[22].beat_interval, -100)
        self.assertEqual(beatmap.timing_points[22].meter, 4)
        self.assertEqual(beatmap.timing_points[22].inherited, True)

        # Test hitobjects
        self.assertEqual(len(beatmap.hitobjects), 102)

        # TODO: test hitobjects
            # TODO: hitobject find & visibility test


    def test_hitobject_visibility_std(self):
        beatmap = BeatmapIO.open_beatmap('unit_tests\\maps\\osu\\test\\abraker - unknown (abraker) [250ms].osu')

        test_data_ar7 = {
            # time : list of objects expected to be visible
            0      : [ 0 ],
            250    : [ 0, 1 ],
            500    : [ 0, 1 ],
            750    : [ 1, 2 ],
            1000   : [ 1, 2 ],
            1250   : [ 2, 3 ],
            1500   : [ 2, 3 ],
            1750   : [ 3, 4 ],
            2000   : [ 3, 4 ],
            2500   : [ 4 ],
            3000   : [  ],
            3250   : [ 5 ],
            4000   : [ 5 ],
            7250   : [ 5, 6 ],
            7500   : [ 5, 6 ],
            8000   : [ 6 ],
            12250  : [ 6, 7 ],
            12500  : [ 6, 7 ],
            13000  : [ 7 ],
            17250  : [ 7, 8 ],
            17500  : [ 7, 8 ],
            18000  : [ 8 ],
            22750  : [ 8, 9 ],
            23500  : [ 9 ],
            32250  : [ 9, 10 ],
            33000  : [ 10 ],
            37500  : [ 10, 11 ],
            38250  : [ 11 ],
            43250  : [ 11, 12 ],
            44000  : [ 12 ],
            46250  : [ 12, 13 ],
            47000  : [ 13 ],
            47500  : [ ],
            48000  : [ ],
            48500  : [ 14 ],
            49250  : [ 14, 15 ],
            49750  : [ 14, 15, 16 ],
            50000  : [ 14, 15, 16 ],
            50250  : [ 14, 16, 17 ],
            50500  : [ 14, 16, 17 ],
            50750  : [ 14, 17, 18 ],
            51000  : [ 14, 17, 18 ],
            51250  : [ 14, 18, 19 ],
            51500  : [ 14, 18, 19 ],
            51750  : [ 14, 19, 20 ],
            52000  : [ 14, 19, 20 ],
            52250  : [ 14, 20 ],
            52500  : [ 14, 20 ],
            52750  : [ 14 ],
            53000  : [ ]
        }

        for test_time, test_obj_idxs in test_data_ar7.items():
            result_objs = Std.get_hitobjects_visible_at_time(beatmap, test_time)
            self.assertEqual(len(result_objs), len(test_obj_idxs), 'Wrong number of objects visible')

            result_obj_idxs = [ beatmap.hitobjects.index(result_obj) for result_obj in result_objs ] 
            for test_obj_idx in test_obj_idxs:
                self.assertTrue(test_obj_idx in result_obj_idxs, 'Wrong object visible')