# QtFusion, AGPL-3.0 license
import cv2
from PySide6 import QtGui, QtCore


def cvImageToQtPixmap(cv_image):
    """
    Converts an OpenCV image to a QPixmap.

    :param cv_image: The OpenCV image to be converted.
    :return: Converted QPixmap.
    """
    cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    height, width, channel = cv_image_rgb.shape
    bytesPerLine = 3 * width
    qt_image = QtGui.QImage(cv_image_rgb.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(qt_image)


def scalePixmap(pixmap, size, keepAspect):
    """
    Scales a QPixmap to a specified size.

    :param pixmap: The QPixmap to be scaled.
    :param size: The QSize to scale the QPixmap to.
    :param keepAspect: Boolean indicating whether to keep the QPixmap's aspect ratio.
    :return: Scaled QPixmap.
    """
    aspectMode = QtCore.Qt.KeepAspectRatio if keepAspect else QtCore.Qt.IgnoreAspectRatio
    return pixmap.scaled(size, aspectMode, QtCore.Qt.SmoothTransformation)
