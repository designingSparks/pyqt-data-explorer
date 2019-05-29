from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import sys


class PlotWidget(pg.GraphicsLayoutWidget):
    
    def __init__(self):
        super().__init__()
        self.myplot = self.addPlot()
        self.viewbox = self.myplot.getViewBox() #correct method
        self.myplot.showGrid(True,True, 1)
        
        x = np.linspace(0,20e-3, 100)
        y = 2*np.sin(2*np.pi*50*x)
        curve = self.myplot.plot(x, y)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    plot = PlotWidget()
    sys.exit(app.exec_())