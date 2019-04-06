from osu.local.beatmap.beatmap import Beatmap



class MapDataProxy():

    full_hitobject_data = None

    @staticmethod
    def set_gamemode(gamemode):
        if gamemode == Beatmap.GAMEMODE_OSU:   from analysis.std.map_data import MapData
        if gamemode == Beatmap.GAMEMODE_MANIA: from analysis.mania.map_data import MapData
        if gamemode == Beatmap.GAMEMODE_OSU:   from analysis.std.map_data import MapData
        if gamemode == Beatmap.GAMEMODE_OSU:   from analysis.std.map_data import MapData

        MapDataProxy.full_hitobject_data = MapData.full_hitobject_data