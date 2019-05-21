'''
'''
from qt import *
import os, sys
from constants import IMAGE_DIR
import pyqtgraph as pg
# from plotwidget import PlotWidget
from plotwidget1 import PlotWidget
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) #Change to NOTSET to disable logging


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Plot Example')
        self.setStyleSheet('QToolBar{spacing:5px;};') #QStatusBar.item {border: none;}
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_height = self.status_bar.minimumSize().height()
        self.status_bar.showMessage('Home view')
        
        self.plotwidget = PlotWidget(updateLabelfn = self.status_bar.showMessage)
        self.createActions()
        self.createToolBar()

        self.plotwidget.viewbox.sigZoomStackEnd.connect(self.forwardAction.setEnabled)
        self.plotwidget.viewbox.sigZoomStackStart.connect(self.backAction.setEnabled)
        self.backAction.setEnabled(False)
        self.forwardAction.setEnabled(False)
        
        self.setCentralWidget(self.plotwidget)
        self.show()
        
        
    def createActions(self):
        '''Toolbar actions'''
        icon = QIcon(os.path.join(IMAGE_DIR, 'back.png'))
        self.backAction = QAction(icon, "Back", self, shortcut=QKeySequence.Back,
                 triggered=self.plotwidget.viewbox.zoom_back)
        
        icon = QIcon(os.path.join(IMAGE_DIR, 'forward.png'))
        self.forwardAction = QAction(icon, "Forward", self, shortcut=QKeySequence.Forward,
                 triggered=self.plotwidget.viewbox.zoom_forward)
        
        icon = QIcon(os.path.join(IMAGE_DIR, 'zoom_fit.png'))
        self.zoomHomeAction = QAction(icon, "Zoom to fit", self, shortcut=QKeySequence.MoveToStartOfLine, #home key
                 triggered=self.plotwidget.viewbox.zoom_home)
        
        icon = QIcon(os.path.join(IMAGE_DIR, 'zoom.png'))
        self.zoomAction = QAction(icon, "Free zoom", self, shortcut="Ctrl+Z",
                 triggered=self.zoom_free)
        self.zoomAction.setCheckable(True)
        
        icon = QIcon(os.path.join(IMAGE_DIR, 'zoom_constrained.png'))
        self.zoomConstrainedAction = QAction(icon, "Constrained zoom", self, shortcut="Ctrl+X",
                 triggered=self.zoom_constrained)
        self.zoomConstrainedAction.setCheckable(True)
        self.zoomConstrainedAction.setChecked(True)

        icon = QIcon(os.path.join(IMAGE_DIR, 'data_cursor.png'))
        self.dataCursorAction = QAction(icon, "Data cursor", self, shortcut="Ctrl+D",
                 triggered=self.show_cursor)
        self.dataCursorAction.setCheckable(True)
        
        iconfile = QIcon(os.path.join(IMAGE_DIR, 'settings_icon.png'))
        self.settingsAction = QAction(iconfile, "&Settings", self, shortcut="Ctrl+,",
                                    triggered=self.settings_action)
        
        self.zoom_action_group = QActionGroup(self)
        self.zoom_action_group.setExclusive(True)
        self.zoom_action_group.addAction(self.zoomAction)
        self.zoom_action_group.addAction(self.zoomConstrainedAction)
        
        
    def createToolBar(self):
        self.toolBar = self.addToolBar("Card")
        self.toolBar.addAction(self.backAction)
        self.toolBar.addAction(self.forwardAction)
        self.toolBar.addAction(self.zoomHomeAction)
        self.toolBar.addAction(self.zoomAction)
        self.toolBar.addAction(self.zoomConstrainedAction)
        self.toolBar.addAction(self.dataCursorAction)
        self.toolBar.addAction(self.settingsAction) 

    def zoom_free(self):
        logger.debug('Setting zoom_free')
        self.plotwidget.viewbox.setZoomMode(pg.ViewBox.freeZoom)
        
    def zoom_constrained(self):
        logger.debug('Setting zoom_constrained')
        self.plotwidget.viewbox.setZoomMode(pg.ViewBox.xZoom)
    
    
    def show_cursor(self):
        show = self.dataCursorAction.isChecked()
        if show:
            logger.debug('Showing cursor')
            self.plotwidget.show_cursor()
        else:
            logger.debug('Hiding cursor')
            self.plotwidget.hide_cursor()
            self.status_bar.showMessage('')
            
    def settings_action(self):
        pass
    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())