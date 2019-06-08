import osrparse
import lzma

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


    # Because the library's parse_string is dun goofed
    # See https://github.com/kszlim/osu-replay-parser/issues/17
    def parse_string(self, replay_data):
        if replay_data[self.offset] == 0x00:
            begin = self.offset = self.offset + Replay.__BYTE

            while replay_data[self.offset] != 0x00: 
                self.offset += Replay.__BYTE
            
            self.offset += Replay.__BYTE
            return replay_data[begin : self.offset-2].decode("utf-8")
        
        elif replay_data[self.offset] == 0x0b:
            self.offset += Replay.__BYTE
            
            string_length = self.__decode(replay_data)
            offset_end    = self.offset + string_length
            string = replay_data[self.offset : offset_end].decode("utf-8")
            
            self.offset = offset_end
            return string

        else:
            #TODO: Replace with custom exception
            raise Exception("Invalid replay")


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
        self.play_data = [ ReplayEvent(int(event[0]), float(event[1]), float(event[2]), int(event[3])) for event in events if int(event[0]) != -12345 ]
        

    def __process_event_times(self):
        time = 0
        for frame in self.play_data:
            time += frame.time_since_previous_action
            frame.t = time
            self.event_times.append(time)