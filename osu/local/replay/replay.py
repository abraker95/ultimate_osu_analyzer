import osrparse
import lzma

from osrparse.replay import ReplayEvent
from osrparse.enums import GameMode
from osu.local.enums import Mod
from misc.math_utils import find


class Replay(osrparse.replay.Replay):

    def __init__(self, replay_data):
        osrparse.replay.Replay.__init__(self, replay_data)
        self.event_times = []


    def is_md5_match(self, md5_hash):
        return self.beatmap_hash == md5_hash


    def get_event_times(self):
        if not self.event_times:
            self.__process_event_times()
        return self.event_times


    def get_data_at_time(self, time):
        idx = find(self.get_event_times(), time)
        return self.play_data[idx]


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

        if self.game_mode == GameMode.Standard:
            events = [ eventstring.split('|') for eventstring in datastring.split(',') ]
            self.play_data = [ReplayEvent(int(event[0]), float(event[1]), float(event[2]), int(event[3])) for event in events]
        else:
            raise NotImplementedError('TODO: replay parsing for other gamemodes')
        
        self.offset = offset_end
        

    def __process_event_times(self):
        time = 0
        for frame in self.play_data:
            time += frame.time_since_previous_action
            self.event_times.append(time)