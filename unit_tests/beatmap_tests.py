from osu.local.beatmap.beatmapIO import BeatmapIO


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