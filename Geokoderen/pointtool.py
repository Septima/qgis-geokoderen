from qgis.gui import QgsMapTool
from PyQt4.QtCore import pyqtSignal


class PointTool(QgsMapTool):
    def __init__(self, canvas, callback):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.callback = callback

    def canvasPressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        # Get the point when the press in map
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        self.callback(point, self.canvas)
        return None

    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        pass

    activated = pyqtSignal()

    def activate(self):
        self.activated.emit()

    deactivated = pyqtSignal()

    def deactivate(self):
        self.deactivated.emit()

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True
