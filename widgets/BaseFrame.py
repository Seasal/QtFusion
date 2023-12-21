# QtFusion, AGPL-3.0 license
import platform
import random
import sys

from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import *
from IMcore.IMencode import imRandCode
from IMcore.IMtrans import ToQtPixmap, scalePixmap, setPixmap
from IMcore.IMwidget import IMDialog, IMainWindow

from .ExtWidgets import *
from .. import __package_name__, __version__, __author__
from ..config.QfConfig import QF_Config
from ..styles import loadYamlSettings
from ..utils.ImageUtils import vertical_bar, horizontal_bar, verticalBar


"""
This package provides a collection of utility functions and classes for enhancing the functionality of PyQt/PySide 
applications. It includes a variety of tools for handling GUI elements, media processing, and style customization in 
a more efficient and simplified manner.

Key Features:
- Decorators for enhancing class functionalities, such as verbose_class for logging class definitions.
- Functions for finding layouts containing specific widgets, replacing widgets with custom classes, and moving widgets 
  to specific positions within a window.
- Utility functions for updating QTableWidget items, loading application settings from YAML files, and applying QSS 
  styles.
- Animation effects for Qt widgets, including fadeIn and zoomIn for creating dynamic UI experiences.
- The FBaseWindow class, providing a base for main application windows with extended functionalities like custom color 
  palettes, stylesheet loading, and UI element state management.
- The FLoginDialog class, offering a customizable login dialog with features such as random verification code generation
   and dynamic tab order setting.
"""
AVATAR = ":/default_icons/default_avatar.png"
COLORS = [[132, 56, 255], [82, 0, 133], [203, 56, 255], [255, 149, 200], [255, 55, 199],
          [72, 249, 10], [146, 204, 23], [61, 219, 134], [26, 147, 52], [0, 212, 187],
          [255, 56, 56], [255, 157, 151], [255, 112, 31], [255, 178, 29], [207, 210, 49],
          [44, 153, 168], [0, 194, 255], [52, 69, 147], [100, 115, 255], [0, 24, 236]]

"""
This package aims to streamline the development of PyQt/PySide applications by offering reusable components and utility
functions that cover common tasks and challenges in GUI application development.
"""


def verbose_class(cls):
    """A decorator for classes to print a message when a class is defined."""
    if QF_Config.VERBOSE:
        print(f"{__package_name__} {__version__} "
              f"Python-{'.'.join(map(str, sys.version_info[:3]))} "
              f"({platform.system()} {platform.release()})")
        # A decorator for classes in the QtFusion package to perform multiple tasks based on the arguments provided.
    return cls


def findContainLayout(widget, layout=None):
    """
    Find the layout containing the given widget.

    :param widget: The widget for which the containing layout is to be found.
    :param layout: The layout to search in. If not provided, it uses the layout of the parent widget of 'widget'.
    :return: The layout containing the 'widget'. If not found, return None.
    """

    if layout is None:
        layout = widget.parentWidget().layout()

    for i in range(layout.count()):
        item = layout.itemAt(i)
        if item.widget() == widget:
            return layout
        elif item.layout():
            result = findContainLayout(widget, item.layout())
            if result:
                return result
    return None


def replaceWidget(original, DerivedClass, properties=["minimumSize", "maximumSize", "objectName", "styleSheet"]):
    """
    Replace a widget with an instance of a derived class, preserving certain properties.

    :param original: The original QWidget instance to be replaced.
    :param DerivedClass: The new class, derived from QWidget, to replace the original widget with.
    :param properties: List of properties to be copied from the original widget to the derived widget.
    :return: The new widget replacing the original one.
    """

    # Create an instance of the derived widget
    derived = DerivedClass()

    # Get the meta object of the original widget
    meta = original.metaObject()

    # Copy the specified properties from the original widget to the derived widget
    for property_name in properties:
        # Get the index of the property
        index = meta.indexOfProperty(property_name)
        if index == -1:
            raise Exception(f"Original widget does not have property '{property_name}'.")

        # Get the QMetaProperty for the property
        prop = meta.property(index)

        # Read the value of the property from the original widget
        value = prop.read(original)

        # Write the value of the property to the derived widget
        if not prop.write(derived, value):
            raise Exception(f"Failed to set property '{property_name}' on derived widget.")

    # Get the layout containing the original widget
    layout = findContainLayout(original)
    if layout:
        # If the original widget is in a layout, replace it in the layout
        for i in range(layout.count()):
            if layout.itemAt(i).widget() == original:
                layout.removeWidget(original)
                layout.insertWidget(i, derived)
    else:
        # If the original widget is not in a layout, we cannot replace it, raise an exception
        raise Exception("Original widget is not in a layout, cannot replace widget.")

    # Delete the original widget
    original.deleteLater()
    return derived


def moveCenter(main_window, msg_box):
    """
    Move a message box to the center of the main window.

    :param main_window: The main window of the application.
    :param msg_box: The message box to be centered.
    """

    mw_frame = main_window.frameGeometry()
    msg_box_frame = msg_box.frameGeometry()

    center_point = mw_frame.center() - QPoint(msg_box_frame.width() / 2, msg_box_frame.height() / 2)
    msg_box.move(center_point)


def addTableItem(tableWidget, row, column, text, alignment=Qt.AlignCenter):
    """
    Add a new item to a QTableWidget.

    :param tableWidget: The QTableWidget to which the new item is to be added.
    :param row: The row number where the new item is to be added.
    :param column: The column number where the new item is to be added.
    :param text: The text of the new item.
    :param alignment: The alignment of the text in the new item.
    """
    newItem = QTableWidgetItem(str(text))
    newItem.setTextAlignment(alignment)
    tableWidget.setItem(row, column, newItem)
    tableWidget.setCurrentItem(newItem)


def updateTable(table_widget, row_number, *row_data):
    """
    Update a specific row in a QTableWidget with new data.

    :param table_widget: The QTableWidget to be updated.
    :param row_number: The row number to be updated.
    :param row_data: The new data for the row. Should match the number of columns in the table.
    :return: The row number after the update.
    """
    column_count = table_widget.columnCount()

    if len(row_data) != column_count - 1:
        raise ValueError(f"Number of arguments does not match the number of columns in the table. "
                         f"Got {len(row_data)} arguments, expected {column_count}.")

    if row_number >= table_widget.rowCount():
        table_widget.setRowCount(row_number + 1)

    row_data = (row_number,) + row_data
    for i, data in enumerate(row_data):
        if isinstance(data, (list, tuple)):
            text = ",".join(map(str, data))
        else:
            text = str(data)
        addTableItem(table_widget, row_number, i, text)

    return row_number + 1


def fadeIn(widget, duration, reverse=False):
    """
    Create a fade-in effect on a QWidget.

    :param widget: The QWidget to apply the fade-in effect to.
    :param duration: The duration of the fade-in effect, in milliseconds.
    :param reverse: If set to True, creates a fade-out effect instead.
    """
    animation = QPropertyAnimation(widget, b"windowOpacity")
    animation.setStartValue(0.0 if not reverse else 1.0)
    animation.setEndValue(1.0 if not reverse else 0.0)
    animation.setDuration(duration)
    animation.start()


def zoomIn(widget, duration, startSize, endSize, reverse=False):
    """
    Create a zoom-in effect on a QWidget.

    :param widget: The QWidget to apply the zoom-in effect to.
    :param duration: The duration of the zoom-in effect, in milliseconds.
    :param startSize: The initial size of the widget for the zoom-in effect.
    :param endSize: The final size of the widget for the zoom-in effect.
    :param reverse: If set to True, creates a zoom-out effect instead.
    """
    animation = QPropertyAnimation(widget, b"size")
    animation.setStartValue(startSize if not reverse else endSize)
    animation.setEndValue(endSize if not reverse else startSize)
    animation.setDuration(duration)
    animation.start()


@verbose_class
class FBaseWindow(IMainWindow):
    """
    FBaseWindow is a class derived from QMainWindow to provide custom methods
    and properties for handling graphical user interface (GUI) related operations
    in the application.
    """

    def __init__(self, parent=None, *args, **kwargs):
        """
        Initializes the FBaseWindow instance.

        :param parent: Parent QWidget. Defaults to None.
        """
        super(FBaseWindow, self).__init__(*args, **kwargs)
        self.mainWindow = parent
        self.user_name = __author__
        self.user_avatar = AVATAR
        self.pre_colors = COLORS

    def init_login_info(self, *args, **kwargs):
        pass

    def init_reg_info(self, *args, **kwargs):
        pass

    def get_cls_color(self, cls_name):
        """
        Returns a list of color codes based on the class name.

        :param cls_name: Class name string.
        :return: List of RGB color codes.
        """
        generated_colors = self.pre_colors if len(cls_name) <= len(self.pre_colors) \
            else [[random.randint(0, 255) for _ in range(3)] for _ in
                  range(len(cls_name))]  # Assign a unique color for each class
        return generated_colors

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        from ..styles.Styles import loadQssStyles
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)

    def set_buttons_enabled(self, enabled):
        """
        Enable or disable all QToolButtons in the current window.

        :param enabled: Boolean value indicating whether to enable or disable the buttons.
        """
        for child in self.findChildren(QToolButton):
            child.setEnabled(enabled)

    def loadYamlSettings(self, yaml_file, base_path="./"):
        """
        Load settings for a QWidget from a YAML file and apply them to the specified window.

        Args:
            yaml_file (str): The file path of the YAML file containing the settings.
            base_path (str, optional): The base path used for resolving relative paths. Default is None.
        """
        loadYamlSettings(self, yaml_file, base_path)

    def showTime(self):
        """
        Method to show the window. The actual implementation needs to be provided.
        """
        self.show()

    def showEvent(self, event):
        """
        Event handler for when the window is shown.

        :param event: Event triggered when the window is shown.
        """
        pass

    def setUiStyle(self, windowFlag=False, transBackFlag=False):
        """
        Sets UI styles and widget states based on the provided flags.

        :param windowFlag: If True, removes window border.
        :param transBackFlag: If True, sets window background to transparent.
        """
        super().setUiStyle(windowFlag, transBackFlag)

    def clearUI(self):
        """
        Clears the UI and reloads settings from a YAML file.
        """
        pass

    def setConfig(self):
        """
        Method to set the configuration of the application. The actual implementation needs to be provided.
        """
        pass

    @staticmethod
    def dispImage(label_display, image, keepAspect=False):
        """
        Displays an image in a QLabel.

        :param label_display: The QLabel to display the image in.
        :param image: The image to be displayed.
        :param keepAspect: Boolean indicating whether to keep the image's aspect ratio. Defaults to False.
        """
        if hasattr(label_display, 'dispImage'):
            label_display.dispImage(image, keepAspect)
        else:
            dispImage(label_display, image, keepAspect)

    @staticmethod
    def setupWidget(widget, properties):
        """
        Set up a QWidget with given properties.

        :param widget: The QWidget to be set up.
        :param properties: A dictionary of properties to set on the QWidget.
        """

        # Loop over each property key-value pair
        for key, value in properties.items():
            # If the widget has an attribute with the name 'key', set its value
            if hasattr(widget, key):
                setattr(widget, key, value)

    def moveToCenter(self):
        """
        Moves the current window to the center of the screen.
        """
        super().moveToCenter()

    def mousePressEvent(self, event):
        """
        Event handler for mouse press event.

        :param event: The mouse event.
        """
        super().mousePressEvent(event)

    def mouseMoveEvent(self, QMouseEvent):
        """
        Event handler for mouse move event.

        :param QMouseEvent: The mouse event.
        """
        super().mouseMoveEvent(QMouseEvent)

    def mouseReleaseEvent(self, QMouseEvent):
        """
        Event handler for mouse release event.

        :param QMouseEvent: The mouse event.
        """
        super().mouseReleaseEvent(QMouseEvent)

    @staticmethod
    def plot_vertical_bar(label, label_name, value, colors=None, color_text="#FFFFFF", alpha=0.7,
                          width=None, height=None, margin=20):
        """
        Plots a vertical bar on a QLabel.

        :param label: The QLabel to plot the bar on.
        :param label_name: The label name.
        :param value: The value for the bar.
        :param colors: The colors for the bar. Defaults to None.
        :param color_text: The color of text.
        :param alpha: The alpha transparency of the bar. Defaults to 0.7.
        :param width: The width of the bar. Defaults to None.
        :param height: The height of the bar. Defaults to None.
        :param margin: The margin for the bar. Defaults to 20.
        """
        if isinstance(label, QLabel):
            width = label.width() if width is None else width  # width
            height = label.height() if height is None else height

            pixmap = vertical_bar(label_name, value, colors, width, height,
                                  color_text=color_text, alpha=alpha, margin=margin)
            label.setPixmap(pixmap)
            label.setScaledContents(True)

    @staticmethod
    def plot_horizontal_bar(label, label_name, value, colors=None, color_text="#FFFFFF",
                            alpha=0.8, width=None, height=None, margin=20):
        """
        Plots a horizontal bar on a QLabel.

        :param label: The QLabel to plot the bar on.
        :param label_name: The label name.
        :param value: The value for the bar.
        :param colors: The colors for the bar. Defaults to None.
        :param color_text: The color of text.
        :param alpha: The alpha transparency of the bar. Defaults to 0.8.
        :param width: The width of the bar. Defaults to None.
        :param height: The height of the bar. Defaults to None.
        :param margin: The margin for the bar. Defaults to 20.
        """
        if isinstance(label, QLabel):
            width = label.width() if width is None else width  # width
            height = label.height() if height is None else height
            pixmap = horizontal_bar(label_name, value, colors, width, height,
                                    color_text=color_text, alpha=alpha, margin=margin)
            label.setPixmap(pixmap)
            label.setScaledContents(True)

    @staticmethod
    def plot_verticalBar(label, label_name, value, colors=None, color_text="#FFFFFF",
                         alpha=0.7, width=None, height=None, margin=20):
        """
        Plots a vertical bar on a QLabel. Seems similar to the 'plot_vertical_bar' method.

        :param label: The QLabel to plot the bar on.
        :param label_name: The label name.
        :param value: The value for the bar.
        :param colors: The colors for the bar. Defaults to None.
        :param color_text: The color of text.
        :param alpha: The alpha transparency of the bar. Defaults to 0.7.
        :param width: The width of the bar. Defaults to None.
        :param height: The height of the bar. Defaults to None.
        :param margin: The margin for the bar. Defaults to 20.
        """
        if isinstance(label, QLabel):
            width = label.width() if width is None else width  # width
            height = label.height() if height is None else height

            pixmap = verticalBar(label_name, value, colors, width, height,
                                 color_text=color_text, alpha=alpha, margin=margin)
            label.setPixmap(pixmap)
            label.setScaledContents(True)


def dispImage(label, image, keepAspect=True):
    """
    Displays an image in a QLabel.
    :param label: The QLabel name.
    :param image: The image to be displayed.
    :param keepAspect: Boolean indicating whether to keep the image's aspect ratio. Defaults to False.
    """
    cv_image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixmap = ToQtPixmap(cv_image_rgb)
    size = label.size()  # get the size of the label display
    pixmap = scalePixmap(pixmap, size, keepAspect)  # scale the pixmap
    setPixmap(label, pixmap)


@verbose_class
class FLoginDialog(IMDialog):
    """
    A custom QDialog class representing a Login Dialog in a GUI application. This class inherits from QDialog.
    """

    def __init__(self, parent=None, *args, **kwargs):
        """
        Initializes the FLoginDialog instance.

        :param parent: The parent widget to the dialog. Default is None.
        """
        super(FLoginDialog, self).__init__(*args, **kwargs)
        self.mainWindow = parent  # A reference to the parent or main window
        self.ver_code = ""  # The verification code for login
        self.avatar = ""  # User avatar
        self.user_name = ""  # Username for login

    def setSlots(self):
        """
        Method to define slots for the Login dialog.
        The actual implementation needs to be provided.
        """
        super().setSlots()
        pass

    def setUiStyle(self, windowFlag=False, transBackFlag=False):
        """
        Sets the user interface style and widget states of the dialog.

        :param windowFlag: If True, removes the border of the dialog.
        :param transBackFlag: If True, makes the dialog's background transparent.
        """
        super().setUiStyle(windowFlag, transBackFlag)

    def generate_random_code(self, widget=None, width=170, height=80, length=4, characters=None):
        """
        Generates a random verification code and returns an image of the code and the code itself as a string.

        :param widget: The widget to set the image on. Defaults to None.
        :param width: The width of the image. Defaults to 170.
        :param height: The height of the image. Defaults to 80.
        :param length: The length of the verification code. Defaults to 4.
        :param characters: The set of characters to use for generating the code. Defaults to digits and uppercase ASCII letters.

        :return: Tuple of the image of the code and the code itself.
        """

        pix, random_str = imRandCode(width, height, length, characters)
        self.ver_code = random_str

        if widget:
            icon = QtGui.QIcon()
            icon.addPixmap(pix, QtGui.QIcon.Normal, QtGui.QIcon.Off)
            widget.setIcon(icon)  # Set the icon of the widget to the generated image

        return pix, random_str

    def set_tab_order(self, *widgets):
        """
        Sets the tab order for the given widgets.

        :param widgets: The widgets to set the tab order for.
        """
        super().set_tab_order(*widgets)

    def show_dialog(self):
        """
        Displays the dialog.
        """
        self.show()

    def minButton(self):
        """
        Minimizes the dialog window.
        """
        self.showMinimized()

    def mousePressEvent(self, event):
        """
        Overriding the mousePressEvent for custom behavior.

        :param event: The mouse press event.
        """
        super().mousePressEvent(event)

    def mouseMoveEvent(self, QMouseEvent):
        """
        Overriding the mouseMoveEvent for custom behavior.

        :param QMouseEvent: The mouse move event.
        """
        super().mouseMoveEvent(QMouseEvent)

    def mouseReleaseEvent(self, QMouseEvent):
        """
        Overriding the mouseReleaseEvent for custom behavior.

        :param QMouseEvent: The mouse release event.
        """
        super().mouseReleaseEvent(QMouseEvent)
