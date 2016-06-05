# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Geokoderen.dk
                                 A QGIS plugin
 Plugin til at åbne et punkt fra QGIS i Geokoderen.dk
                              -------------------
        begin                : 2015-10-22
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Septima P/S
        email                : kontakt@septima.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os.path
import webbrowser
from PyQt4.QtCore import (
    QSettings,
    QTranslator,
    qVersion,
    QCoreApplication
)
from PyQt4.QtGui import (
    QAction,
    QIcon,
    QMessageBox
)
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from .pointtool import PointTool
# Initialize Qt resources from file resources.py
import resources


class Geokoderen(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Geokoderen_{}.qm'.format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Geokoderen.dk')

        self.icon_active = QIcon(':plugins/Geokoderen/icon_active.png')
        self.icon = QIcon(':plugins/Geokoderen/icon.png')

        # Defining if the pointtool is active or not
        self.pointtool_active = False

        # Initialize the pointool
        self.pointtool = PointTool(
            self.iface.mapCanvas(),
            self.open_geokoderen
        )

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        return QCoreApplication.translate('Geokoderen', message)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        # Initialize main button
        icon = QIcon(':/plugins/Geokoderen/icon.png')
        self.geokoderen_action = QAction(
            icon,
            self.tr(u'Aktiver knappen, tryk herefter i kortet for at åbne i Geokoderen.dk'),
            self.iface.mainWindow()
        )
        self.geokoderen_action.triggered.connect(self.run)
        self.geokoderen_action.setEnabled(True)
        # add action to plugin menu
        self.iface.addPluginToMenu(self.menu, self.geokoderen_action)
        # Add button to toolbar
        self.iface.addToolBarIcon(self.geokoderen_action)
        # add to self.action for proper deletion
        self.actions.append(self.geokoderen_action)

        # Initialize about menu
        self.about_action = QAction(
            self.tr(u'Om pluginet'),
            self.iface.mainWindow()
        )
        self.about_action.triggered.connect(self.open_about_dialog)
        self.about_action.setEnabled(True)
        # Add action to plugin menu
        self.iface.addPluginToMenu(self.menu, self.about_action)
        # add to self.action for proper deletion
        self.actions.append(self.about_action)

        self.pointtool.activated.connect(self.set_icon_active)
        self.pointtool.deactivated.connect(self.set_icon_inactive)

    def set_icon_active(self):
        self.actions[0].setIcon(self.icon_active)

    def set_icon_inactive(self):
        self.actions[0].setIcon(self.icon)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Geokoderen'),
                action
            )
            self.iface.removeToolBarIcon(action)

    def open_about_dialog(self):
        about = self.tr(
            u'Geokoderen.dk til QGIS lader brugeren åbne et punkt fra '
            u'kortet i <a href="http://geokoderen.dk">geokoderen.dk</a>.<br />'
            u'<br />'
            u'Udviklet af: Septima P/S<br />'
            u'Mail: '
            u'<a href="mailto:kontakt@septima.dk">kontakt@septima.dk</a><br />'
            u'Web: <a href="http://septima.dk">septima.dk</a><br />'
            u'<br />'
            u'''Icons made by
                <a href="http://www.freepik.com" title="Freepik">Freepik</a>
                from <a href="http://www.flaticon.com"
                        title="Flaticon">www.flaticon.com</a> is licensed by
                <a href="http://creativecommons.org/licenses/by/3.0/"
                   title="Creative Commons BY 3.0">CC BY 3.0</a>.'''
        )
        QMessageBox.information(
            self.iface.mainWindow(), 'Om Geokoderen.dk', about
        )

    def run(self):
        """Run method that performs all the real work"""
        if self.pointtool_active:
            self.iface.mapCanvas().unsetMapTool(self.pointtool)
            self.pointtool_active = False
        else:
            self.pointtool_active = True
            self.iface.mapCanvas().setMapTool(self.pointtool)

    def open_geokoderen(self, point, canvas):
        # Get the current crs
        src_crs = canvas.mapRenderer().destinationCrs()
        # Define the destination crs
        dst_crs = QgsCoordinateReferenceSystem(25832)
        # Create a transformer from current to destination
        xform = QgsCoordinateTransform(src_crs, dst_crs)

        # Transform from current crs to UTM32N
        transformed_point = xform.transform(point)
        bgk_url = 'https://www.geokoderen.dk/#centrum={x},{y}'.format(
            x=transformed_point.x(),
            y=transformed_point.y()
        )
        # Opens the url in the default webbrowser on OS
        webbrowser.open_new(bgk_url)
        # Deactive the button again
        self.iface.mapCanvas().unsetMapTool(self.pointtool)
        # Set the tool to not active
        self.pointtool_active = False
