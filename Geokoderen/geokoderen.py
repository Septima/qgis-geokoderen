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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QMessageBox
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsCoordinateTransform
from pointtool import PointTool
# Initialize Qt resources from file resources.py
import resources
import os.path
import webbrowser


class Geokoderen:
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

        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Geokoderen.dk')
        self.toolbar.setObjectName(u'Geokoderen.dk')

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

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action
            )

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Geokoderen/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Aktiver knappen, tryk herefter i kortet for at åbne i Geokoderen.dk'),
            callback=self.run,
            parent=self.iface.mainWindow()
        )

        self.add_action(
            None,
            text=self.tr(u'Om pluginet'),
            callback=self.open_about_dialog,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False
        )

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
        # remove the toolbar
        del self.toolbar

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
