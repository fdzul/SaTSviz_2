# -*- coding: utf-8 -*-
"""
/***************************************************************************
 satsviz
                                 A QGIS plugin
 SaTSViz aims to provide QGIS an additional feature of analysis by utilising SaTScan. All input files needed for SaTScan are created by the plugin and the output files from it are read by the plugin and fed in to QGIS to visualise the analysis results. The plugin provides benefit to both the software's
                             -------------------
        begin                : 2015-06-24
        copyright            : (C) 2015 by Vasuda Trehan under guidance of Shiva Reddy Koti
        email                : vasudatrehan@gmail.com
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
    """Load satsviz class from file satsviz.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .detect_satsviz import satsviz
    return satsviz(iface)
