#How to display cross hairs.
#https://groups.google.com/forum/?fromgroups#!topic/pyqtgraph/zP-NjbuzOQc
#https://groups.google.com/forum/?fromgroups#!topic/pyqtgraph/TGVqAalIfS4

# In Eclipse, add the local pyqtgraph project dir as an external library to the PyDev PYTHONPATH or
# import sys
# sys.path.insert(0, '../../pyqtgraph')

from qt import *
import pyqtgraph as pg
print(pg.__file__)
# import pyqtgraph.exporters
import numpy as np
import os, sys
import time
import threading
from eng_notation import eng

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) #Change to NOTSET to disable logging

class PlotWidget(pg.GraphicsLayoutWidget):
    
    def __init__(self, updateLabelfn=None):
        super().__init__()
        self.updateLabelfn = updateLabelfn
        self.setWindowTitle('Plot Widget')

        self.myplot = self.addPlot()
        self.myplot.showGrid(x=True,y=True)

        self.viewbox = self.myplot.getViewBox()
        self.viewbox.setMouseMode(pg.ViewBox.RectMode) #one button mode
        self.viewbox.setZoomMode(pg.ViewBox.xZoom)
        
        #Cursor and dot
        self.cursor = pg.CursorLine(angle=90, movable=True)
        self.cursor.sigPositionChanged.connect(self.updatePlotHighlight)
        self.plotHighlight = pg.ScatterPlotItem(size=10, pen={"color": "#8080ff"}, brush="#000000")
        
        
        self.setCentralWidget(self.myplot)
        self.show()
        self.get_data()


    def get_data(self):
        t = ConnectThread(100) #executes self.ble_wrapper.connect(self.selected_uuid)
        t.setDaemon(True)
        t.finished.connect(self.plot_data)
        t.start()

    def plot_data(self, y):
        self.xdata = np.linspace(0, 20e-3, 100)
        self.ydata = y
        self.myplot.plot(self.xdata, self.ydata)
        self.viewbox.initZoomStack()

    def show_cursor(self):
        #Get the current viewbox limits
        left = self.viewbox.viewRange()[0][0]
        right = self.viewbox.viewRange()[0][1]
        middle = np.average([left, right])
        self.myplot.addItem(self.cursor, ignoreBounds=True)
        self.myplot.addItem(self.plotHighlight, ignoreBounds=True)
        
        
        idx = (np.abs(self.xdata - middle)).argmin()
        xpos = self.xdata[idx]
        self.cursor.setPos(pg.Point(xpos,0))
        self.updatePlotHighlight(middle)
        
    def hide_cursor(self):
        self.myplot.removeItem(self.cursor)
        self.myplot.removeItem(self.plotHighlight)
        
    @Slot(float)
    def updatePlotHighlight(self, xpos):
        
        idx = (np.abs(self.xdata - xpos)).argmin()
        highlight_x = self.xdata[idx]
        highlight_y = self.ydata[idx]
        self.plotHighlight.setData([highlight_x], [highlight_y])
        
        if self.updateLabelfn is not None:
            label_str = 'x={}, y={}'.format(eng(highlight_x), eng(highlight_y))
            self.updateLabelfn(label_str)
        
        
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