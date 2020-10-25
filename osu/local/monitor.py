import watchdog.observers
import watchdog.events
import os



class Monitor(watchdog.observers.Observer):

    def __init__(self, osu_path):
        watchdog.observers.Observer.__init__(self)

        if not os.path.exists(osu_path):
            raise Exception(f'"{osu_path}" does not exist!')

        self.osu_path = osu_path
        self.monitors = {}
        self.start()


    def __del__(self):
        self.stop()   


    def create_replay_monitor(self, name, callback):
        replay_path = f'{self.osu_path}/data/r'
        if not os.path.exists(replay_path):
            raise Exception(f'"{replay_path}" does not exist!')

        class EventHandler(watchdog.events.FileSystemEventHandler):
            def on_created(self, event): 
                if '.osr' in event.src_path:
                    callback(event.src_path)

        print(f'Created file creation monitor for {self.osu_path}/data/r')
        self.monitors[name] = self.schedule(EventHandler(), replay_path, recursive=False)


    def create_map_montor(self, name, callback, beatmap_path):
        # TODO
        pass