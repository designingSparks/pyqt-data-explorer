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