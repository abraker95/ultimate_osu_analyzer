import pyqtgraph
from pyqtgraph import QtCore, QtGui


class AimPlot(pyqtgraph.GraphicsObject):
    def __init__(self, t, d, cs_px, yoffset=0, color=(100, 100, 255, 100)):
        pyqtgraph.GraphicsObject.__init__(self)

        self.t = t           # times
        self.d = d           # distances
        self.cs_px = cs_px   # circle size in osu!px

        self.yoffset = yoffset
        self.color = color

        self.px_h = self.pixelHeight()
        self.px_w = self.pixelWidth()
        
        self.generatePicture()
    

    def update_data(self, t, d, cs_px):
        self.t = t           # times
        self.d = d           # distances
        self.cs_px = cs_px   # circle size in osu!px

        self.px_h = self.pixelHeight()
        self.px_w = self.pixelWidth()

        self.generatePicture()


    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()

        p = QtGui.QPainter(self.picture)
        p.setPen(pyqtgraph.mkPen(color=self.color))

        # This 20x aligns it right on the boundary of slider rendering in hitobject_plot if yoffset is +1 or -1
        y_mid  = 25*self.px_h*self.yoffset

        radius_x = 20*self.px_w/self.cs_px
        radius_y = 20*self.px_h/self.cs_px

        # Render
        for t, d in zip(self.t, self.d):
            p.drawEllipse(QtCore.QPointF(t, y_mid), d*radius_x, d*radius_y)

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
        px_w = self.pixelWidth()

        # Without pixel_height the render scales with how the view is zoomed in/out
        if self.px_h != px_h or self.px_w != px_w:
            self.px_h = px_h
            self.px_w = px_w

            self.generatePicture()