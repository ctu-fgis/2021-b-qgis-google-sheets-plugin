# coding=utf-8
"""DockWidget test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'marek.hoffmann@fsv.cvut.cz, monika.krizova@fsv.cvut.cz'
__date__ = '2021-06-04'
__copyright__ = 'Copyright 2021, Group B - FGIS 2021'

import unittest

from qgis.PyQt.QtGui import QDockWidget

from google_sheets_downloader2_dockwidget import GoogleSheetsDownloader2DockWidget

from utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class GoogleSheetsDownloader2DockWidgetTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.dockwidget = GoogleSheetsDownloader2DockWidget(None)

    def tearDown(self):
        """Runs after each test."""
        self.dockwidget = None

    def test_dockwidget_ok(self):
        """Test we can click OK."""
        pass

if __name__ == "__main__":
    suite = unittest.makeSuite(GoogleSheetsDownloader2DialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

