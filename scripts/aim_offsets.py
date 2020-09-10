import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui


"""
Visualizes aim offsets for all hits
"""
class AimOffsets():

    # Construct a unit radius circle for the graph
    class HitCicle(QtGui.QGraphicsObject):
        def __init__(self, center=(0.0, 0.0), radius=1.0, pen=QtGui.QPen()):
            QtGui.QGraphicsObject.__init__(self)
            self.center = center
            self.radius = radius
            self.pen = pen

            self.pen.setBrush(QtCore.Qt.white)
            self.pen.setWidth(0.1)

        def boundingRect(self):
            rect = QtCore.QRectF(0, 0, 2*self.radius, 2*self.radius)
            rect.moveCenter(QtCore.QPointF(*self.center))
            return rect

        def paint(self, painter, option, widget):
            painter.setPen(self.pen)
            painter.drawEllipse(self.boundingRect())


    def run(self):
        map_data    = StdMapData.get_map_data(get_beatmap().hitobjects)
        replay_data = StdReplayData.get_replay_data(get_replays()[0].play_data)
        score_data  = StdScoreData.get_score_data(replay_data, map_data)

        aim_x_offsets = StdScoreData.aim_x_offsets(score_data)
        aim_y_offsets = StdScoreData.aim_y_offsets(score_data)

        # Draw a circle
        cs = get_beatmap().difficulty.cs
        cs_px = (109 - 9*cs)/2

        fig, ax = plt.subplots()
        ax.add_artist(matplotlib.patches.Circle((0, 0), radius=cs_px, color='#8080FE', fill=False))

        # Draw points
        plt.scatter(aim_x_offsets, aim_y_offsets, s=1)
        plt.title('Aim offsets')

        plt.xlim(-cs_px*1.5, cs_px*1.5)
        plt.ylim(-cs_px*1.5, cs_px*1.5)

        plt.show()


    def run2(self, replay_idx):
        self.__init_gui_elements()
        self.__construct_gui()
        self.__set_data(replay_idx)

        self.win.show()
        return self.win


    def __init_gui_elements(self):
        self.win = QtGui.QMainWindow()
        
        self.aim_scatterplot_widget = pyqtgraph.PlotWidget(title='Aim scatterplot')
        self.aim_plot = self.aim_scatterplot_widget.plot()


    def __construct_gui(self):
        self.win.setCentralWidget(self.aim_scatterplot_widget)


    def __set_data(self, replay_idx):
        self.win.setWindowTitle(get_beatmap().metadata.name + ' ' + get_replays()[replay_idx].get_name())

        # Data extraction
        map_data    = StdMapData.get_map_data(get_beatmap().hitobjects)
        replay_data = StdReplayData.get_replay_data(get_replays()[replay_idx].play_data)
        score_data  = StdScoreData.get_score_data(replay_data, map_data)

        aim_x_offsets = StdScoreData.aim_x_offsets(score_data)
        aim_y_offsets = StdScoreData.aim_y_offsets(score_data)

        # Draw a circle
        cs = get_beatmap().difficulty.cs
        cs_px = (109 - 9*cs)/2

        self.aim_scatterplot_widget.addItem(AimOffsets.HitCicle((0, 0), cs_px))
        self.aim_plot.setData(aim_x_offsets.values, aim_y_offsets.values, pen=None, symbol='o', symbolPen=None, symbolSize=2, symbolBrush=(100, 100, 255, 200))