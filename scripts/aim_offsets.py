map_data    = StdMapData.get_aimpoint_data(get_beatmap().hitobjects)
replay_data = get_replays()[0]
score_data  = StdScoreData.get_score_data(replay_data, map_data)

aimoffset_data = score_data[:, 3]
aimoffset_data = np.dstack(aimoffset_data)[0]

# Draw a circle
cs = get_beatmap().difficulty.cs
cs_px = (109 - 9*cs)/2

fig, ax = plt.subplots()
ax.add_artist(matplotlib.patches.Circle((0, 0), radius=cs_px, color='#8080FE', fill=False))

# Draw points
plt.scatter(aimoffset_data[0], aimoffset_data[1], s=1)
plt.title('Aim offsets')

plt.xlim(-cs_px*1.5, cs_px*1.5)
plt.ylim(-cs_px*1.5, cs_px*1.5)

plt.show()