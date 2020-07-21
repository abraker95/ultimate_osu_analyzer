def play(start_ms=get_beatmap().get_time_range()[0], end_ms=get_beatmap().get_time_range()[1], skip=50):
    play.stop = False

    def run(start_ms, end_ms, skip):
        for i in range(start_ms, end_ms, skip):
            timeline.timeline_marker.setPos(i)
            tick()

            if play.stop: break

    CmdUtils.threaded(run, (start_ms, end_ms, skip))