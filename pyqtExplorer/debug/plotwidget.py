#How to display cross hairs.
#https://groups.google.com/forum/?fromgroups#!topic/pyqtgraph/zP-NjbuzOQc
#https://groups.google.com/forum/?fromgroups#!topic/pyqtgraph/TGVqAalIfS4

#Allow the local pyqtgraph package to be found
import sys
sys.path.insert(0, '../../pyqtgraph')

from qt import *
import pyqtgraph as pg
from pyqtgraph import LinearRegionItem
import numpy as np
import os, sys
import time
import threading
import logging
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) #Change to NOTSET to disable logging
print(pg.__file__)


class PlotWidget(pg.GraphicsLayoutWidget):
    
    x_dir = 0
    y_dir = 1
    
    def __init__(self):
        super().__init__()
        # self.setWindowTitle('Plot Widget')
        self.myplot = self.addPlot()
        self.viewbox = self.myplot.getViewBox()
        self.viewbox.setMouseEnabled(x=False, y=False)
        # plt = pg.plot(x, y, title=theTitle, pen='r')
        self.myplot.showGrid(x=True,y=True)
        self.myscene = self.myplot.scene()
        
        #Need to assign proxes to self
        self.proxy1 = pg.SignalProxy(self.myplot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved) 
        # self.proxy2 = pg.SignalProxy(self.myplot.scene().sigMouseClicked, rateLimit=60, slot=self.mouseClicked) 
        # self.plotscene = self.myplot.scene()
        # self.plotscene.sigMouseClicked.connect(self.onMouseClick)
        self.myplot.scene().sigMouseClicked.connect(self.onMouseClick)
        self.hregion = None #highlights zoom region
        self.vregion = None #highlights zoom region
        self.zoom_mode = 'xy' #or 'rect'
        self.zoom_direction = None
        
        #cross hair
#         self.vline = pg.InfiniteLine(angle=90, movable=False)
#         self.hline = pg.InfiniteLine(angle=0, movable=False)
        # self.myplot.addItem(self.vline, ignoreBounds=True)
        # self.myplot.addItem(self.hline, ignoreBounds=True)

        # self.setCentralWidget(self.myplot)
        self.show()
        self.isMoving = False
        self._startCoord = None #graph coordinates
        self._startPos = None #screen coordinates
        self.moved = False
        
        self.t = np.linspace(0, 20e-3, 100)
        self.zoom_stack = list() #list of tuples: 'xMin', 'xMax', 'yMin', 'yMax'
        self.zoom_pos = 0
        self.get_data()
        
        #ROI test
#         pen = QPen(Qt.green, 0.1) #https://doc.qt.io/qt-5/qpen.html#details
        self.roi = pg.ROI((0,0), (10e-3, 1), pen=None)
        # self.roi.setBrush(Qt.Red)
        self.myplot.addItem(self.roi)
        
        
    def mousePressEvent(self, event):
        pos = event.pos()
        point = self.viewbox.mapSceneToView(pos)
        x = point.x()
        y = point.y()
        print('MousePressEvent x={}, y={}'.format(x,y))
        self._startCoord = point #graph coordinate
        self._startPos = pos #screen coordinate
        
        
#         self.hregion = pg.LinearRegionItem()
        # self.myplot.addItem(self.vline1, ignoreBounds=True)
#         self.myplot.addItem(self.vregion, ignoreBounds=True)
        # self.vline1.setPos(x)
        
        #Comment out to disable zoom using LinearRegionItem
        if QApplication.keyboardModifiers() == Qt.ControlModifier: #zoom in vertical direction
            self.zoom_direction = self.y_dir
            self.vregion = pg.LinearRegionItem(orientation=LinearRegionItem.Horizontal)
            starty = self._startCoord.y()
            self.vregion.setRegion((starty, starty))
            self.myplot.addItem(self.vregion, ignoreBounds=True)
        else: #zoom in horizontal dir
            self.zoom_direction = self.x_dir
            self.hregion = pg.LinearRegionItem(orientation=LinearRegionItem.Vertical)
            startx = self._startCoord.x()
            self.hregion.setRegion((startx, startx))
            self.myplot.addItem(self.hregion, ignoreBounds=True)
         
                    
        return QGraphicsView.mousePressEvent(self, event)   


    

    def onMouseClick(self, event):
        '''
        Not the same as mouse release event. Only called if the mouse wasn't moved.
        '''
        logger.debug('onMouseClick')
        pos = event.scenePos()
        point = self.viewbox.mapSceneToView(pos)
        x = point.x()
        y = point.y()
        print(x, y)
        #This works
        # self.viewbox.setLimits(xMin=min(self.t), xMax=max(self.t))

        
    def mouseMoved(self, event):
        self.moved = True
        pos = event[0]
        # print(pos)
        point = self.viewbox.mapSceneToView(pos)
        
        
        
        if self._startCoord is not None:
            
            #Calculate delta in graph coordinates
#             delta = point - self._startCoord
#             dx = delta.x()
#             dy = delta.y()
#             logger.debug('dx={}, dy={}'.format(dx, dy))
            
            #Calculate delta in screen coordinates to determine zoom direction in xy zoom mode
            delta = pos - self._startPos
            dx = delta.x()
            dy = delta.y()
        
        
            if abs(dx) > abs(dy):
                
                if self.zoom_direction != self.x_dir:
                    logger.debug('Zoom X')
#                     logger.debug('Screen: dx={}, dy={}'.format(dx, dy))
#                     self.zoom_direction = self.x_dir
                    
#                     self.myscene.removeItem(self.vregion)
#                     self.hregion = pg.LinearRegionItem(orientation=LinearRegionItem.Vertical)
#                     startx = self._startCoord.x()
#                     self.hregion.setRegion((startx, startx))
#                     self.myplot.addItem(self.hregion, ignoreBounds=True)
            else:
                if self.zoom_direction != self.y_dir:
                    logger.debug('Zoom Y')
#                     logger.debug('Screen: dx={}, dy={}'.format(dx, dy))
#                     self.zoom_direction = self.y_dir
                    
#                     self.myscene.removeItem(self.hregion)
#                     self.vregion = pg.LinearRegionItem(orientation=LinearRegionItem.Horizontal)
#                     starty = self._startCoord.y()
#                     self.vregion.setRegion((starty, starty))
#                     self.myplot.addItem(self.vregion, ignoreBounds=True)
                    
                

        #Map to data coordinates 
        x = point.x()
        y = point.y()
        # print(x,y)
        # self.vline.setPos(x) 
        # self.hline.setPos(y)

    
        
    
    def mouseReleaseEvent(self, event):
        '''
        Release after a drag.
        '''
        pos = event.pos()
        point = self.viewbox.mapSceneToView(pos)
        x = point.x()
        y = point.y()
        logger.debug('mouseReleaseEvent x={}, y={}'.format(x,y))

        point = self.viewbox.mapSceneToView(pos)

        # self.myplot.addItem(self.vline2, ignoreBounds=True)
        # self.vline2.setPos(x)
#         scene = self.myplot.scene()
        
        
        self.myscene.removeItem(self.hregion)
        self.myscene.removeItem(self.vregion)
        
        
        if self.moved:
            
            #If a zoom back was previously pressed, remove items ahead in the zoom stack
            n = len(self.zoom_stack) - self.zoom_pos - 1
            if n:
                logger.debug('Pruning zoom stack. n={}'.format(n))
                self.zoom_stack = self.zoom_stack[:self.zoom_pos+1]
                
                
            if self.zoom_direction == self.x_dir:
                xmin = min(point.x(), self._startCoord.x())
                xmax = max(point.x(), self._startCoord.x())
                ybounds = self.viewbox.viewRange()[1]
                ymin = ybounds[0]
                ymax = ybounds[1]
                
            elif self.zoom_direction ==  self.y_dir:
                xbounds = self.viewbox.viewRange()[0]
                xmin = xbounds[0]
                xmax = xbounds[1]
                ymin = min(point.y(), self._startCoord.y())
                ymax = max(point.y(), self._startCoord.y())
                
            elif self.zoom_direction is None: #debug
                xbounds = self.viewbox.viewRange()[0]
                xmin = xbounds[0]
                xmax = xbounds[1]
                ybounds = self.viewbox.viewRange()[1]
                ymin = ybounds[0]
                ymax = ybounds[1]
                
#             xmin = min(point.x(), self._startCoord.x())
#             xmax = max(point.x(), self._startCoord.x())

            #Perform zoom
            self.viewbox.setLimits(xMin=xmin, xMax=xmax, yMin=ymin, yMax=ymax)
            
            # self.viewbox.setLimits(minXRange=xmin, maxXRange=xmax)
            self.moved = False
            
            point = (xmin, xmax, ymin, ymax)
            self.zoom_stack.append(point) #'xMin', 'xMax', 'yMin', 'yMax'
            self.zoom_pos += 1
            logger.debug('Updated zoom stack: {}. zoom_pos: {}, len zoom_stack: {}'.format(point, self.zoom_pos, len(self.zoom_stack)))
            
        return QGraphicsView.mouseReleaseEvent(self, event) 
 
 
    def zoom_back(self):
        
        if self.zoom_pos > 0:
            self.zoom_pos -= 1
            last_pos = self.zoom_stack[self.zoom_pos]
            self.viewbox.setLimits(xMin=last_pos[0], xMax=last_pos[1], yMin=last_pos[2], yMax=last_pos[3])
            logger.debug('Zoomed back. zoom_pos: {}, len zoom_stack: {}'.format(self.zoom_pos, len(self.zoom_stack)))
        else:
            logger.debug('Start of zoom stack reached. zoom_pos: {}'.format(self.zoom_pos))
            


    def zoom_forward(self):
        logger.debug('Zoom forward')
        if self.zoom_pos < (len(self.zoom_stack) - 1):
            self.zoom_pos += 1
            last_pos = self.zoom_stack[self.zoom_pos]
            self.viewbox.setLimits(xMin=last_pos[0], xMax=last_pos[1], yMin=last_pos[2], yMax=last_pos[3])
            logger.debug('Zoomed forward. zoom_pos: {}, len zoom_stack: {}'.format(self.zoom_pos, len(self.zoom_stack)))
        else:
            logger.debug('End of zoom stack reached. zoom_pos: {}, len zoom_stack: {}'.format(self.zoom_pos, len(self.zoom_stack)))

    def zoom_home(self):
        logger.debug('Zooming home')
        
        
    def get_data(self):
        t = ConnectThread(100) #executes self.ble_wrapper.connect(self.selected_uuid)
        t.setDaemon(True)
        t.finished.connect(self.plot_data)
        t.start()

    def plot_data(self, y):
        
        self.myplot.plot(self.t, y)
        self.y = y
        
        xbounds = self.viewbox.viewRange()[0]
        xmin = xbounds[0]
        xmax = xbounds[1]
        ybounds = self.viewbox.viewRange()[1]
        ymin = ybounds[0]
        ymax = ybounds[1]
        point = (xmin, xmax, ymin, ymax)
        self.zoom_stack.append(point)


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