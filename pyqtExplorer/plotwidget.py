#How to display cross hairs.
#https://groups.google.com/forum/?fromgroups#!topic/pyqtgraph/zP-NjbuzOQc
#https://groups.google.com/forum/?fromgroups#!topic/pyqtgraph/TGVqAalIfS4
from qt import *
import pyqtgraph as pg
import numpy as np
import os, sys
import time
import threading


class PlotWidget(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle('Plot Widget')
        self.myplot = self.addPlot()
        self.viewbox = self.myplot.getViewBox()
        self.viewbox.setMouseEnabled(x=False, y=False)
        # plt = pg.plot(x, y, title=theTitle, pen='r')
        self.myplot.showGrid(x=True,y=True)

        #Need to assign proxes to self
        self.proxy1 = pg.SignalProxy(self.myplot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved) 
        # self.proxy2 = pg.SignalProxy(self.myplot.scene().sigMouseClicked, rateLimit=60, slot=self.mouseClicked) 

        # self.plotscene = self.myplot.scene()
        # self.plotscene.sigMouseClicked.connect(self.onMouseClick)
        self.myplot.scene().sigMouseClicked.connect(self.onMouseClick)

        self.myplot.scene().sigMouseMoved

        self.viewbox = self.myplot.getViewBox()
        #cross hair
        self.vline = pg.InfiniteLine(angle=90, movable=False)
        # self.vline1 = pg.InfiniteLine(angle=90, movable=False)
        # self.vline2 = pg.InfiniteLine(angle=90, movable=False)
        self.hline = pg.InfiniteLine(angle=0, movable=False)
        # self.myplot.addItem(self.vline, ignoreBounds=True)
        # self.myplot.addItem(self.hline, ignoreBounds=True)

        # self.setCentralWidget(self.myplot)
        self.show()
        self.get_data()
        self.isMoving = False
        self._startCoord = None
        self.moved = False

    # def mouseDragEvent(self, event):
    #     print('mouseDragEvent')

    # def mouseClicked(self, event):
    #     print('mouseClicked')
    def mousePressEvent(self, event):
        pos = event.pos()
        point = self.viewbox.mapSceneToView(pos)
        x = point.x()
        y = point.y()
        print('MousePressEvent x={}, y={}'.format(x,y))
        self.startx = x
        # self.starty = y
        

        self._startCoord = point
        self.hregion = pg.LinearRegionItem()


        # self.myplot.addItem(self.vline1, ignoreBounds=True)
        self.myplot.addItem(self.hregion, ignoreBounds=True)
        # self.vline1.setPos(x)
        self.hregion.setRegion((self.startx, self.startx))
        return QGraphicsView.mousePressEvent(self, event)   

    def mouseReleaseEvent(self, event):   
        pos = event.pos()
        point = self.viewbox.mapSceneToView(pos)
        x = point.x()
        y = point.y()
        print('mouseReleaseEvent x={}, y={}'.format(x,y))


        point = self.viewbox.mapSceneToView(pos)

        
            

        # self.myplot.addItem(self.vline2, ignoreBounds=True)
        # self.vline2.setPos(x)
        scene = self.myplot.scene()
        scene.removeItem(self.hregion)
        # self.removeItem(self.hregion)
        if self.moved:

            xmin = min(point.x(), self._startCoord.x())
            xmax = max(point.x(), self._startCoord.x())


            self.viewbox.setLimits(xMin=xmin, xMax=xmax)
            # self.viewbox.setLimits(minXRange=xmin, maxXRange=xmax)
            self.moved = False
        return QGraphicsView.mouseReleaseEvent(self, event) 

    def onMouseClick(self, event):
        '''
        Not the same as mouse release event
        '''
        print('onMouseClick')
        pos = event.scenePos()
        point = self.viewbox.mapSceneToView(pos)
        x = point.x()
        y = point.y()
        print(x, y)
        #This works
        # self.viewbox.setLimits(xMin=min(self.t), xMax=max(self.t))

    def mouseMoved(self, evt):
        self.moved = True
        pos = evt[0]
        # print(pos)
        point = self.viewbox.mapSceneToView(pos)

        if self._startCoord is not None:
            delta = point - self._startCoord
            dx = delta.x()
            dy = delta.y()
            print('dx={}, dy={}'.format(dx, dy))

        #Map to data coordinates 
        x = point.x()
        y = point.y()
        # print(x,y)
        # self.vline.setPos(x) 
        # self.hline.setPos(y)

        

    def get_data(self):
        t = ConnectThread(100) #executes self.ble_wrapper.connect(self.selected_uuid)
        t.setDaemon(True)
        t.finished.connect(self.plot_data)
        t.start()

    def plot_data(self, y):
        self.t = np.linspace(0, 20e-3, 100)
        self.myplot.plot(self.t, y)
        self.y = y


class ConnectThread(threading.Thread, QObject):
    
    finished = Signal(list)
    
    def __init__(self, npoints):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.npoints = npoints
        
    def run(self):
        t = np.linspace(0, 20e-3, self.npoints)
        y = 2*np.sin(2*np.pi*50*t)
        self.finished.emit(list(y))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plot = PlotWidget()
    sys.exit(app.exec_())