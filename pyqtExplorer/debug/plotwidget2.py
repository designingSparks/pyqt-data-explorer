#How to display cross hairs.
#https://groups.google.com/forum/?fromgroups#!topic/pyqtgraph/zP-NjbuzOQc
#https://groups.google.com/forum/?fromgroups#!topic/pyqtgraph/TGVqAalIfS4

#https://github.com/pyqtgraph/pyqtgraph/blob/9aaae8d5dc86d5373d297f5763ab65d8043afcdb/pyqtgraph/graphicsItems/ViewBox/ViewBox.py
import sys
sys.path.insert(0, '../../pyqtgraph')
from qt import *
import pyqtgraph as pg
from pyqtgraph import functions as fn
from pyqtgraph.graphicsItems.ViewBox.ViewBox import ChildGroup
import numpy as np
import os, sys
import time
import threading
print(pg.__file__)

class PlotWidget(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Plot Widget')

        self.myplot = self.addPlot()
        self.myplot.showGrid(x=True,y=True)
        proxy = pg.SignalProxy(self.myplot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved) 
        self.myplot.proxy = proxy

        self.viewbox = self.myplot.getViewBox()
        self.viewbox.setMouseEnabled(x=False, y=False)
        
        #Not working.
        self.childGroup = ChildGroup(self.myplot)
        self.childGroup.itemsChangedListeners.append(self)
        
        #Scale box
#         self.rbScaleBox = QGraphicsRectItem(0, 0, 0.01, 1) #coordinate system
#         self.rbScaleBox.setPen(fn.mkPen((255,255,100), width=1))
#         self.rbScaleBox.setBrush(fn.mkBrush(255,255,0,100))
#         self.rbScaleBox.setZValue(1e9)
# #         self.rbScaleBox.hide()
#         self.myplot.addItem(self.rbScaleBox, ignoreBounds=True)
        
        self.start_pos = None
        
        #cross hair
        self.vline = pg.InfiniteLine(angle=90, movable=False)
        self.hline = pg.InfiniteLine(angle=0, movable=False)
        self.myplot.addItem(self.vline, ignoreBounds=True)
        self.myplot.addItem(self.hline, ignoreBounds=True)
        self.show()
        self.get_data()


    def mousePressEvent(self, event):
        self.start_pos = event.pos()
        print('Mouse press detected')
        return QGraphicsView.mousePressEvent(self, event)   
    
#     def mouseDragEvent(self, ev, axis=None):
#         print('Drag')
#         return QGraphicsView.mouseDragEvent(self, ev) 

#     def updateScaleBox(self, p1, p2):
#         r = QRectF(p1, p2)
#         r = self.childGroup.mapRectFromParent(r)
#         self.rbScaleBox.setPos(r.topLeft())
#         self.rbScaleBox.resetTransform()
#         self.rbScaleBox.scale(r.width(), r.height())
#         self.rbScaleBox.show()
        
    def mouseMoved(self, qpoint):
        
        pos = qpoint[0]
#         if ev.button() & Qt.LeftButton:
#             print(pos)

#         if self.start_pos is not None:
#             self.updateScaleBox(self.start_pos, qpoint)
        
        #Map to data coordinates 
        point = self.viewbox.mapSceneToView(pos)
        print(point.x(), point.y())
        self.vline.setPos(point.x()) 
        self.hline.setPos(point.y()) 

    def get_data(self):
        t = ConnectThread(100) #executes self.ble_wrapper.connect(self.selected_uuid)
        t.setDaemon(True)
        t.finished.connect(self.plot_data)
        t.start()

    def plot_data(self, y):
        t = np.linspace(0, 20e-3, 100)
        self.myplot.plot(t, y)


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