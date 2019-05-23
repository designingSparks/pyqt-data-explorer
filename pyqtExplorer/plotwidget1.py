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
import bokeh.palettes as pal
'''
Don't set as the central widget otherwise resizing won't work!
'''
from constants import LINEWIDTH
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) #Change to NOTSET to disable logging
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOption('antialias', True) #Plotted curve looks nicer

class PlotWidget(pg.GraphicsLayoutWidget):
    
    def __init__(self, updateLabelfn=None):
        super().__init__()
        self.updateLabelfn = updateLabelfn
        self.setWindowTitle('Plot Widget')
        self.ci.layout.setContentsMargins(0,25,30,20) #left, top, right, bottom
        

        self.myplot = self.addPlot()
        
#         self.myplot = self.addPlot(axisItems = {'left', 'right'})
        self.viewbox = self.myplot.getViewBox() #correct method
#         self.viewbox.setBackgroundColor((192,192,192))
        [ self.myplot.getAxis(ax).setZValue(1000) for ax in self.myplot.axes ] #Otherwise setBackgroundColor paints over the axis lines
        #Could also directly patch PlotItem.axis.setZValue(-1000) to 1
        self.myplot.showGrid(True, True, 0.5)
#         self.myplot.showGrid(x=True,y=True) 
        self.viewbox.setMouseMode(pg.ViewBox.RectMode) #one button mode
        self.viewbox.setZoomMode(pg.ViewBox.xZoom)
        
        #Cursor and dot
        self.cursor = pg.CursorLine(angle=90, movable=True)
        self.cursor.sigPositionChanged.connect(self.updatePlotHighlight)
        self.plotHighlight = pg.ScatterPlotItem(size=10, pen={"color": "#8080ff"}, brush="#000000")
        
#         self.resize(800,800)
#         self.viewbox.resize(800,800)
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
        
        #https://bokeh.pydata.org/en/0.10.0/docs/reference/palettes.html
#         mypen = pg.functions.mkPen({'color': pal.Blues[6][0], 'width': 1.5}) #blue
#         mypen = pg.functions.mkPen({'color': pal.BuPu[6][0], 'width': 1.5}) #magenta
        
        #https://bokeh.pydata.org/en/latest/docs/reference/palettes.html
        mypen = pg.functions.mkPen({'color': pal.RdBu[8][0], 'width': LINEWIDTH})
        self.myplot.plot(self.xdata, self.ydata, pen=mypen)
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