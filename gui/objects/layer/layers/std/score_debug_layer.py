from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from analysis.osu.std.replay_data import StdReplayData
from analysis.osu.std.map_data import StdMapData
from analysis.osu.std.score_data import StdScoreData

from misc.math_utils import *
from generic.temporal import Temporal
from gui.objects.layer.layer import Layer

from osu.local.hitobject.std.std import Std



class StdScoreDebugLayer(Layer, Temporal):

    viewable_time_interval = 1000   # ms

    def __init__(self, data, time_updater):
        Layer.__init__(self, 'Score debug layer')
        Temporal.__init__(self)

        beatmap, replay = data
        
        self.aimpoint_data = StdMapData.get_aimpoint_data(beatmap.hitobjects)
        self.replay_data   = StdReplayData.get_event_data(replay.play_data)
        self.score_data    = StdScoreData.get_score_data(self.replay_data, self.aimpoint_data)
        
        time_updater.connect(self.time_changed)
        self.time_changed.connect(lambda time: self.layer_changed())


    def paint(self, painter, option, widget):
        if not self.time: return
        if len(self.score_data) <= 0: return

        self.ratio_x = widget.width()/Std.PLAYFIELD_WIDTH
        self.ratio_y = widget.height()/Std.PLAYFIELD_HEIGHT

        painter.setPen(QColor(255, 0, 0, 255))

        start_idx = find(self.score_data, self.time - StdScoreDebugLayer.viewable_time_interval, selector=lambda event: event[0])
        end_idx   = find(self.score_data, self.time, selector=lambda event: event[0])
        end_idx   = min(end_idx + 1, len(self.score_data))

        for score in self.score_data[start_idx:end_idx]:
            pos_x, pos_y = score[1]
            offset       = score[2]

            painter.drawText(pos_x*self.ratio_x, pos_y*self.ratio_y, str(offset))
