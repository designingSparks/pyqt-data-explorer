#!/usr/bin/env python3

from PyQt5 import QtWidgets
import pyqtgraph as pg
import numpy as np
pg.setConfigOption('background', 'w')
# pg.setConfigOption('foreground', 'k')
# pg.setConfigOption('antialias', True) #Plotted curve looks nicer

class TestPlot(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        self.plotItem = self.addPlot()
        self.plotItem.showGrid(x=True,y=True)
        self.viewbox = self.plotItem.getViewBox()
        self.viewbox2 = self.plotItem.getViewBox2()
        self.viewbox2.setZValue(-1001)
        self.viewbox2.setBackgroundColor((192,192,192))
        
        self.plotItem.getAxis("bottom").setPen({"color": (255, 255, 255), "width": 2})
        self.plotItem.getAxis("left").setPen({"color": (255, 255, 255), "width": 2})
        self.plot = self.plotItem.plot(np.random.rand(10), pen={"color": (0, 0, 0), "width": 3})
        print(self.format_graphicsitem_tree(self.plotItem))

    def format_graphicsitem_tree(self, gitem, newline=False):
        returnstring = "{}: {}\n".format(gitem.zValue(), gitem)
        for child in gitem.childItems():
            returnstring += "  {}\n".format(self.format_graphicsitem_tree(child).replace("\n", "\n  "))
        return returnstring.rpartition("\n")[0]
 
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = TestPlot()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()