import osrparse
from misc.math_utils import find


class Replay():

    def __init__(self, filepath=None):
        self.replay = None
        if filepath:
            self.replay = osrparse.parse_replay_file(filepath)

        self.event_times = []


    def is_md5_match(self, md5_hash):
        return self.replay.beatmap_hash == md5_hash


    def get_event_times(self):
        if not self.event_times:
            self.__process_event_times()
        return self.event_times


    def get_data_at_time(self, time):
        idx = find(self.get_event_times(), time)
        return self.replay.play_data[idx]


    def __process_event_times(self):
        time = 0
        for frame in self.replay.play_data:
            time += frame.time_since_previous_action
            self.event_times.append(time)