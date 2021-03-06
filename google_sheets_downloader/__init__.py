# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GoogleSheetsDownloader
                                 A QGIS plugin
 This plugin downloads data from Google Sheets
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-06-04
        copyright            : (C) 2021 by Group B - FGIS 2021
        email                : marek.hoffmann@fsv.cvut.cz, monika.krizova@fsv.cvut.cz
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GoogleSheetsDownloader2 class from file GoogleSheetsDownloader2.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .google_sheets_downloader import GoogleSheetsDownloader
    return GoogleSheetsDownloader(iface)
