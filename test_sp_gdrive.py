import os
import sys
os.chdir(QgsProject.instance().readPath("./"))
filepath = os.getcwd()

sys.path.insert(0, filepath)
from sp_gdrive import download, loadVector

filename = 'eq-data.csv'

download(filepath, filename)
loadVector(filepath, filename)