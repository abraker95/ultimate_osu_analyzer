map_data    = StdMapData.get_aimpoint_data(get_beatmap().hitobjects)
replay_data = get_replays()[0]
score_data  = StdScoreData.get_score_data(replay_data, map_data)

hitoffset_data = score_data[:, 2]
aimoffset_data = score_data[:, 3]

plt.hist(hitoffset_data, 20)
plt.xlabel('offset from 0 ms')
plt.ylabel('number of hits')
plt.show()