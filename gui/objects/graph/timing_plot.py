import pyqtgraph
from pyqtgraph import QtCore, QtGui


class TimingPlot(pyqtgraph.GraphicsObject):
    def __init__(self, ts, te, yoffset=0, color=(100, 100, 255, 100)):
        pyqtgraph.GraphicsObject.__init__(self)

        self.ts = ts    # start times
        self.te = te    # end times

        self.yoffset = yoffset
        self.color = color

        self.px_h = self.pixelHeight()
        self.generatePicture()
    

    def update_data(self, ts, te):
        self.ts = ts    # start times
        self.te = te    # end times
        self.px_h = self.pixelHeight()

        self.generatePicture()


    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()

        p = QtGui.QPainter(self.picture)
        p.setPen(pyqtgraph.mkPen(color=self.color))

        # This 20x aligns it right on the boundary of slider rendering in hitobject_plot if yoffset is +1 or -1
        # Make it 25x so the horizontal line is visible
        y_mid = 25*self.px_h*self.yoffset

        # Calc the height of the vertical lines
        # If the |---| is on top of the notes, then make the top part shorter
        # If the |---| is on bottom of the notes, then make the bottom part shorter
        if self.yoffset < 0:
            y_top = 25*self.px_h
            y_btm = -12.5*self.px_h
        elif self.yoffset == 0:
            y_top =  25*self.px_h
            y_btm = -25*self.px_h
        else:
            y_top = 12.5*self.px_h
            y_btm = -25*self.px_h

        # Render
        for ts, te in zip(self.ts, self.te):
            p.drawLine(QtCore.QPointF(ts, y_btm + y_mid), QtCore.QPointF(ts, y_top + y_mid))
            p.drawLine(QtCore.QPointF(ts,     0 + y_mid), QtCore.QPointF(te,     0 + y_mid))
            p.drawLine(QtCore.QPointF(te, y_btm + y_mid), QtCore.QPointF(te, y_top + y_mid))

        p.end()
    

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())


    def viewRangeChanged(self):
        """
        Called whenever the view coordinates of the ViewBox containing this item have changed.
        """
        px_h = self.pixelHeight()

        # Without pixel_height the render scales with how the view is zoomed in/out
        if self.px_h != px_h:
            self.px_h = px_h
            self.generatePicture()