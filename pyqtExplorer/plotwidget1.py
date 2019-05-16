#How to display cross hairs.
#https://groups.google.com/forum/?fromgroups#!topic/pyqtgraph/zP-NjbuzOQc
#https://groups.google.com/forum/?fromgroups#!topic/pyqtgraph/TGVqAalIfS4
from qt import *
import pyqtgraph as pg
# import pyqtgraph.exporters
import numpy as np
import os, sys
import time
import threading


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Plot Widget')

        self.myplot = pg.PlotWidget()
        self.myplot.showGrid(x=True,y=True)
        proxy = pg.SignalProxy(self.myplot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved) 
        self.myplot.proxy = proxy

        self.viewbox = self.myplot.getViewBox()
        #cross hair
        self.vline = pg.InfiniteLine(angle=90, movable=False)
        self.hline = pg.InfiniteLine(angle=0, movable=False)
        self.myplot.addItem(self.vline, ignoreBounds=True)
        self.myplot.addItem(self.hline, ignoreBounds=True)
        self.setCentralWidget(self.myplot)
        self.show()
        self.get_data()

    def mouseMoved(self, evt):
        pos = evt[0]
        print(pos)

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
    mainWindow = MainWindow()
    sys.exit(app.exec_())