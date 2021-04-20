import os
import sys
os.chdir(QgsProject.instance().readPath("./"))
filepath = os.getcwd()

sys.path.insert(0, filepath)
from sp_gdrive import loadVector, downloadSpreadsheet

filename = 'eq-data_GSheets'
downloadSpreadsheet(filepath, filename)
loadVector(filepath, filename)