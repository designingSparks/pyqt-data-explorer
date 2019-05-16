'''
'''
from qt import *
import os, sys
from constants import IMAGE_DIR
from plotwidget import PlotWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Plot Example')
        self.setStyleSheet('QToolBar{spacing:5px;};') #QStatusBar.item {border: none;}
        self.createActions()
        self.createToolBar()
        self.plotwidget = PlotWidget()

        self.setCentralWidget(self.plotwidget)
        self.show()
        
        
    def createActions(self):
        '''
        Toolbar actions
        '''
        icon = QIcon(os.path.join(IMAGE_DIR, 'zoom.png'))
        self.zoomAction = QAction(icon, "&Zoom", self, shortcut="Ctrl+Z",
                 triggered=self.zoom)
        
        icon = QIcon(os.path.join(IMAGE_DIR, 'zoom_constrained.png'))
        self.zoomConstrainedAction = QAction(icon, "Zoom &Constrained", self, shortcut="Ctrl+X",
                 triggered=self.zoom_constrained)

        iconfile = QIcon(os.path.join(IMAGE_DIR, 'settings_icon.png'))
        self.settingsAction = QAction(iconfile, "&Settings", self, shortcut="Ctrl+,",
                                    triggered=self.settings_action)

    
    def createToolBar(self):
        self.toolBar = self.addToolBar("Card")
        self.toolBar.addAction(self.zoomAction)
        self.toolBar.addAction(self.zoomConstrainedAction)
        self.toolBar.addAction(self.settingsAction) 
        
    def zoom(self):
        pass
    
    def zoom_constrained(self):
        pass
    
    def settings_action(self):
        pass
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())