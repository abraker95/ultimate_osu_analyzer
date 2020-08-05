

class HitOffsets():

    def run(self):
        map_data = ManiaActionData.get_map_data(get_beatmap().hitobjects)
        press_durr = ManiaMapMetrics.data_to_press_durations(map_data)
        press_durr = press_durr.to_numpy().flatten()

        # Filter out 0's because that's the default value for none
        press_durr = press_durr[press_durr != 0]

        # We don't care the press interval is too high
        press_durr = press_durr[press_durr < 1000]
                
        add_graph_2d_data('Press intervals', (30, press_durr), plot_type=BAR_PLOT)
