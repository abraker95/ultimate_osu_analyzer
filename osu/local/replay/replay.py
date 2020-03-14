import math
import osrparse
import lzma

from osu.local.hitobject.std.std import Std
from osu.local.hitobject.mania.mania import Mania

from osrparse.replay import ReplayEvent
from osrparse.enums import GameMode
from osu.local.enums import Mod
from misc.math_utils import find


# \FIXME: Try out new and old replays. There seems to be a discrepency between them here:
#         https://github.com/ppy/osu/blob/master/osu.Game/Scoring/Legacy/LegacyScoreParser.cs#L78
class Replay(osrparse.replay.Replay):

    def __init__(self, replay_data):
        osrparse.replay.Replay.__init__(self, replay_data)
        self.event_times = []

        self.__process_event_times()


    def is_md5_match(self, md5_hash):
        return self.beatmap_hash == md5_hash


    def get_name(self):
        player_mods = self.player_name + ' ' + self.get_mods_name()
        score_acc   = str(self.score) + ' (x' + str(self.max_combo) + ', ' + str(self.get_acc()) + '%)'
        hits_misses = str(self.number_300s + self.gekis) + '/' + str(self.number_100s + self.katus) + '/' + str(self.number_50s) + '/' + str(self.misses)
        return player_mods + ' - ' + score_acc + ' | ' + hits_misses


    def get_acc(self):
        if self.game_mode == GameMode.Standard:
            acc = 100*Std.get_acc_from_hits(self.number_300s + self.gekis, self.number_100s + self.katus, self.number_50s, self.misses)

        if self.game_mode == GameMode.Taiko:
            acc = -1
            # TODO
            pass

        if self.game_mode == GameMode.CatchTheBeat:
            acc = -1
            # TODO
            pass

        if self.game_mode == GameMode.Osumania:
            acc = 100*Mania.get_acc_from_hits(self.number_300s + self.gekis, self.katus, self.number_100s, self.number_50s, self.misses)

        return round(acc, 3)


    def get_mods_name(self):
        if Mod.NoMod in self.mod_combination: return ''
        mods_str = '+'

        if Mod.Hidden in self.mod_combination:      mods_str += 'HD'
        if Mod.DoubleTime in self.mod_combination:  mods_str += 'DT'
        if Mod.Nightcore in self.mod_combination:   mods_str += 'NC'
        if Mod.HalfTime in self.mod_combination:    mods_str += 'HT'
        if Mod.HardRock in self.mod_combination:    mods_str += 'HR'
        if Mod.Easy in self.mod_combination:        mods_str += 'EZ'
        if Mod.SuddenDeath in self.mod_combination: mods_str += 'SD'
        if Mod.Perfect in self.mod_combination:     mods_str += 'PF'
        if Mod.Flashlight in self.mod_combination:  mods_str += 'FL'
        if Mod.NoFail in self.mod_combination:      mods_str += 'NF'
        if Mod.Relax in self.mod_combination:       mods_str += 'RX'
        if Mod.Autopilot in self.mod_combination:   mods_str += 'AP'

        return mods_str


    def get_event_times(self):
        if not self.event_times:
            self.__process_event_times()
        return self.event_times


    def get_data_at_time(self, time, selector=None):
        idx = find(self.get_event_times(), time, selector=selector)
        return self.play_data[idx]


    def get_data_at_time_range(self, time_start, time_end, selector=None):
        idx_start = find(self.get_event_times(), time_start, selector=selector)
        idx_end   = find(self.get_event_times(), time_end, selector=selector)
        return self.play_data[idx_start : idx_end]


    def parse_life_bar_graph(self, replay_data):
        # Apperently there is a special exception if life bar data is blank
        if replay_data[self.offset] == 0x0B:
            self.life_bar_graph = self.parse_string(replay_data)
        else:
            self.offset += Replay.__BYTE

        # I don't even... 
        # A replay that's missing game version number is weird, but
        # until I come across another case like this that doesn't work,
        # this is to allow the Leaf - I replay to load
        if self.game_version == 0:
            self.offset += Replay.__BYTE
    # Because the library's parse_string is dun goofed
    # See https://github.com/kszlim/osu-replay-parser/issues/17
    def parse_string(self, replay_data):
        if replay_data[self.offset] == 0x00:
            begin = self.offset = self.offset + Replay.__BYTE

            while replay_data[self.offset] != 0x00: 
                self.offset += Replay.__BYTE
            
            self.offset += Replay.__BYTE
            return replay_data[begin : self.offset - 2].decode("utf-8")
        
        elif replay_data[self.offset] == 0x0b:
            self.offset += Replay.__BYTE
            
            string_length = self.__decode(replay_data)
            offset_end    = self.offset + string_length
            string = replay_data[self.offset : offset_end].decode("utf-8")
            
            self.offset = offset_end
            return string

        else:
            #TODO: Replace with custom exception
            raise Exception(f'Invalid replay\noffset: {self.offset}\nData: {replay_data[self.offset]}')


    # Because library didn't update to include ScoreV2 mod
    # See https://github.com/kszlim/osu-replay-parser/issues/18
    def parse_mod_combination(self):
        # Generator yielding value of each bit in an integer if it's set + value
        # of LSB no matter what .
        def bits(n):
            if n == 0:
                yield 0
            while n:
                b = n & (~n+1)
                yield b
                n ^= b

        bit_values_gen = bits(self.mod_combination)
        self.mod_combination = frozenset(Mod(mod_val) for mod_val in bit_values_gen)


    # Because library doesn't support non std gamemodes
    def parse_play_data(self, replay_data):
        offset_end = self.offset + self.__replay_length
        datastring = lzma.decompress(replay_data[self.offset : offset_end], format=lzma.FORMAT_AUTO).decode('ascii')[:-1]
        self.offset = offset_end

        events = [ eventstring.split('|') for eventstring in datastring.split(',') ]

        if self.game_mode == GameMode.Standard and Mod.HardRock in self.mod_combination:
            self.play_data = [ ReplayEvent(int(event[0]), float(event[1]), Std.PLAYFIELD_HEIGHT - float(event[2]), int(event[3])) for event in events if int(event[0]) != -12345 ]
        else:
            self.play_data = [ ReplayEvent(int(event[0]), float(event[1]), float(event[2]), int(event[3])) for event in events if int(event[0]) != -12345 ]
        
        if self.game_mode == GameMode.Osumania:
            # Calculate number of keys used in the replay for mania
            largest_key_event = max(self.play_data, key=lambda event: event.x)
            self.mania_keys = int(math.log(largest_key_event.x, 2)/2)
        

    def __process_event_times(self):
        time = 0
        for frame in self.play_data:
            time += frame.time_since_previous_action
            frame.t = time
            self.event_times.append(time)