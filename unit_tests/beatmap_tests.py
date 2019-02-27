from misc.math_utils import *
from osu.local.beatmap.beatmapIO import BeatmapIO
from osu.local.beatmap.beatmap_utility import BeatmapUtil


class BeatmapTests():

    @staticmethod
    def test_beatmap_loading_mania(filepath):
        beatmap = BeatmapIO(filepath)
        
        # Test metadata
        assert beatmap.metadata.beatmap_format == 14, 'beatmap_format = (%s)' % str(beatmap.metadata.beatmap_format)
        assert beatmap.metadata.title == 'GHOST', 'title = (%s)' % str(beatmap.metadata.title)
        assert beatmap.metadata.artist == 'Camellia', 'artist = (%s)' % str(beatmap.metadata.artist)
        assert beatmap.metadata.version == 'Collab PHANTASM [MX]', 'version = (%s)' % str(beatmap.metadata.version)
        assert beatmap.metadata.creator == 'qqqant', 'creator = (%s)' % str(beatmap.metadata.creator)

        # Test timing points
        assert len(beatmap.timing_points) == 179, '# timing points = (%s)' % str(len(beatmap.timing_points))

        assert beatmap.timing_points[0].offset == 8527, 'offset = (%s)' % str(beatmap.timing_points[0].offset)
        assert beatmap.timing_points[0].beat_interval == 272.727272727273, 'beat_interval = (%s)' % str(beatmap.timing_points[0].beat_interval)
        assert beatmap.timing_points[0].meter == 4, 'meter = (%s)' % str(beatmap.timing_points[0].meter)
        assert beatmap.timing_points[0].inherited == False, 'inherited = (%s)' % str(beatmap.timing_points[0].inherited)

        assert beatmap.timing_points[178].offset == 316163, 'offset = (%s)' % str(beatmap.timing_points[178].offset)
        assert beatmap.timing_points[178].beat_interval == -125, 'beat_interval = (%s)' % str(beatmap.timing_points[178].beat_interval)
        assert beatmap.timing_points[178].meter == 4, 'meter = (%s)' % str(beatmap.timing_points[178].meter)
        assert beatmap.timing_points[178].inherited == True, 'inherited = (%s)' % str(beatmap.timing_points[178].inherited)

        # Test hitobjects
        assert len(beatmap.hitobjects) == 3004, '# hitobjects = (%s)' % str(len(beatmap.hitobjects))

        # TODO: test hitobjects


    @staticmethod
    def test_beatmap_loading_std(filepath):
        beatmap = BeatmapIO(filepath)
        
        # Test metadata
        assert beatmap.metadata.beatmap_format == 9, 'beatmap_format = (%s)' % str(beatmap.metadata.beatmap_format)
        assert beatmap.metadata.title == 'Red Goose', 'title = (%s)' % str(beatmap.metadata.title)
        assert beatmap.metadata.artist == 'Mutsuhiko Izumi', 'artist = (%s)' % str(beatmap.metadata.artist)
        assert beatmap.metadata.version == 'ERT Basic', 'version = (%s)' % str(beatmap.metadata.version)
        assert beatmap.metadata.creator == 'nold_1702', 'creator = (%s)' % str(beatmap.metadata.creator)

        # Test timing points
        assert len(beatmap.timing_points) == 23, '# timing points = (%s)' % str(len(beatmap.timing_points))

        assert beatmap.timing_points[0].offset == -401, 'offset = (%s)' % str(beatmap.timing_points[0].offset)
        assert beatmap.timing_points[0].beat_interval == 300, 'beat_interval = (%s)' % str(beatmap.timing_points[0].beat_interval)
        assert beatmap.timing_points[0].meter == 4, 'meter = (%s)' % str(beatmap.timing_points[0].meter)
        assert beatmap.timing_points[0].inherited == False, 'inherited = (%s)' % str(beatmap.timing_points[0].inherited)

        assert beatmap.timing_points[22].offset == 117799, 'offset = (%s)' % str(beatmap.timing_points[22].offset)
        assert beatmap.timing_points[22].beat_interval == -100, 'beat_interval = (%s)' % str(beatmap.timing_points[22].beat_interval)
        assert beatmap.timing_points[22].meter == 4, 'meter = (%s)' % str(beatmap.timing_points[22].meter)
        assert beatmap.timing_points[22].inherited == True, 'inherited = (%s)' % str(beatmap.timing_points[22].inherited)

        # Test hitobjects
        assert len(beatmap.hitobjects) == 102, '# hitobjects = (%s)' % str(len(beatmap.hitobjects))

        # TODO: test hitobjects
            # TODO: hitobject find & visibility test


    @staticmethod
    def test_hitobject_visibility_std():
        beatmap = BeatmapIO('unit_tests\\abraker - unknown (abraker) [250ms].osu')

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
            result_objs = BeatmapUtil.get_hitobjects_visible_at_time(beatmap, test_time)
            assert len(result_objs) == len(test_obj_idxs), 'Wrong number of objects visible at t=%s; Expected: %s,  Result: %s' % (test_time, str(len(test_obj_idxs)), str(len(result_objs)))

            result_obj_idxs = [ beatmap.hitobjects.index(result_obj) for result_obj in result_objs ] 
            for test_obj_idx in test_obj_idxs:
                assert test_obj_idx in result_obj_idxs, 'Wrong object visible at t=%s; Expected index: %s,  Resultant list: %s' % (test_time, str(test_obj_idx), str(result_obj_idxs))