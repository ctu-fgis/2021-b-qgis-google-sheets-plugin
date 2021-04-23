import os
import sys
os.chdir(QgsProject.instance().readPath("./"))
filepath = os.getcwd()

sys.path.insert(0, filepath)
from sp_gdrive import loadVector, downloadSpreadsheet

filename = 'body'
Xcol = 'X'
Ycol = 'Y'
EPSG = "epsg:4326"
downloadSpreadsheet(filepath, filename)
loadVector(filepath, filename, Xcol, Ycol, EPSG)