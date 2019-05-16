'''
'''
import os, sys

#Needed for cx_freeze
if hasattr(sys, "frozen"): #if is a cx_freeze app
    this_file = os.path.realpath(sys.executable)
    BASEDIR = os.path.dirname(this_file)
else:
    this_file = os.path.realpath(sys.argv[0])
    BASEDIR = os.path.dirname(this_file)
    
IMAGE_DIR = os.path.join(BASEDIR, 'images')


#Logger setup
import logging
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s.%(msecs)d    %(name)-12s %(levelname)-8s %(message)s', '%H:%M:%S') #includes ms
#     formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
root_logger = logging.getLogger('')
root_logger.addHandler(console) 

#Package logger can be useful if you are using other packages that have verbose logs that you want to turn off
# logger = logging.getLogger('log') #log is the name of the package logger.

'''
To use the logger in a python file:
import logging
logger = logging.getLogger('log.' + __name__) #package logger OR
logger = logging.getLogger(__name__) #root logger
logger.setLevel(logging.DEBUG) #Change to NOTSET to disable logging
'''