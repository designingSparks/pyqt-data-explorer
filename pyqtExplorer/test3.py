from PyQt5 import QtWidgets
import pyqtgraph as pg
import numpy as np

class TestPlot(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        self.curveData = np.random.rand(200)
        self.plotItem = self.addPlot()
        self.plotDataItem = self.plotItem.plot(self.curveData)
        self.plotHighlight = pg.ScatterPlotItem(size=10, pen={"color": "#8080ff"}, brush="#000000")
        self.plotItem.addItem(self.plotHighlight, ignoreBounds=True)
        self.plotLabel = pg.TextItem("X", anchor=(0.5, 1.0))
        self.plotItem.addItem(self.plotLabel, ignoreBounds=True)
        self.setWindowTitle('My Plot')
        self.selected_x_i = 0
        # Create the infinite line to indicate an x coordinate
        self.crosshairx = pg.InfiniteLine(angle=90, movable=False, pen={"color": "#8080ff"})
        self.plotItem.addItem(self.crosshairx, ignoreBounds=True)

        self.signalproxy = pg.SignalProxy(self.plotItem.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

    def mouseMoved(self, event):
        pos = event[0]  ## using signal proxy turns original arguments into a tuple
        if self.plotItem.sceneBoundingRect().contains(pos):
            mousePoint = self.plotItem.getViewBox().mapSceneToView(pos)
            index = int(mousePoint.x())
            if (index > 0 and index < self.curveData.shape[0] and
                mousePoint.y() >= self.plotItem.getViewBox().viewRange()[1][0] and
                mousePoint.y() <= self.plotItem.getViewBox().viewRange()[1][1]):
                #self.crosshairx.label.setFormat("{:0.2f}".format(self.curveData[index]))s
                self.crosshairx.setPos(mousePoint.x())
                self.plotHighlight.setData([index], [self.curveData[index]])
                self.plotLabel.setPos(index, self.curveData[index])
                self.plotLabel.setText("{:0.2g}".format(self.curveData[index]))
            else:
                # Could proably hide the crosshair in better way...
                self.crosshairx.setPos(self.plotItem.getViewBox().viewRange()[0][0] - 1)
                self.plotHighlight.clear()
                self.plotLabel.setText("")

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = TestPlot()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()