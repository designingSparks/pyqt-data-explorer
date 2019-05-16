'''
'''
QT_API = 'PYQT5' #

if QT_API == 'PYSIDE2':
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
elif QT_API == 'PYQT5':
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    Signal = pyqtSignal
    Slot = pyqtSlot
    
try: 
    from PyQt5.QtCore import pyqtWrapperType as wrappertype
except ImportError:
    from sip import wrappertype