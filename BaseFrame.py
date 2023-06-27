# QtFusion, AGPL-3.0 license
import random
import string

import yaml
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QImage
from PySide6.QtWidgets import *
from captcha.image import ImageCaptcha

from .ExtWidgets import *
from .ImageUtils import vertical_bar, horizontal_bar, verticalBar


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


def loadYamlSettings(window, yaml_file):
    """
    Load settings for a QMainWindow from a YAML file.

    :param window: The QMainWindow to which the settings are to be applied.
    :param yaml_file: The path of the YAML file containing the settings.
    """
    with open(yaml_file, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)

    for widget_name, settings in yaml_data.items():
        widget_type = eval(settings['type'])
        widget = window.findChild(widget_type, widget_name)

        if widget is not None:
            if 'text' in settings:
                widget.setText(settings['text'])

            if 'icon' in settings:
                icon = QIcon()
                icon.addPixmap(QPixmap(settings['icon']), QIcon.Normal, QIcon.Off)
                widget.setIcon(icon)

            if 'background' in settings:
                widget.setStyleSheet(f"#{widget_name} {{ border-image: url({settings['background']}) }}")

            if 'windowIcon' in settings:
                icon = QIcon()
                icon.addPixmap(QPixmap(settings['windowIcon']), QIcon.Normal, QIcon.Off)
                widget.setWindowIcon(icon)


def loadQssStyles(window, qss_file):
    """
    Load QSS styles for a QMainWindow from a QSS file.

    :param window: The QMainWindow to which the styles are to be applied.
    :param qss_file: The path of the QSS file containing the styles.
    """
    with open(qss_file, 'r', encoding='utf-8') as file:
        qss_data = file.read()
    window.setStyleSheet(qss_data)


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


class FBaseWindow(QMainWindow):
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
        self.mainWindow = parent   # Reference to the main window of the application
        self.user_name = "Seasal Wesley"  # User name for the application
        self.user_avatar = ":/default_icons/default_avatar.png"  # Default avatar image path
        # Predefined color palette, each color represented as an RGB triplet
        self.pre_colors = [[132, 56, 255], [82, 0, 133], [203, 56, 255], [255, 149, 200], [255, 55, 199],
                           [72, 249, 10], [146, 204, 23], [61, 219, 134], [26, 147, 52], [0, 212, 187],
                           [255, 56, 56], [255, 157, 151], [255, 112, 31], [255, 178, 29], [207, 210, 49],
                           [44, 153, 168], [0, 194, 255], [52, 69, 147], [100, 115, 255], [0, 24, 236]]

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
                  range(len(cls_name))]   # Assign a unique color for each class
        return generated_colors

    def loadStyleSheet(self, qssFilePath):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        """
        with open(qssFilePath, "r", encoding='utf-8') as f:
            styleSheet = f.read()
        self.setStyleSheet(styleSheet)  # Set the application's style sheet to the contents of the file

    def set_buttons_enabled(self, enabled):
        """
        Enable or disable all QToolButtons in the current window.

        :param enabled: Boolean value indicating whether to enable or disable the buttons.
        """
        for child in self.findChildren(QToolButton):
            child.setEnabled(enabled)

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
        if windowFlag:
            self.setWindowFlags(Qt.FramelessWindowHint)
        if transBackFlag:
            self.setAttribute(Qt.WA_TranslucentBackground)
        self.moveToCenter()  # 将窗口移动至中心

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
            if keepAspect:
                aspectMode = QtCore.Qt.KeepAspectRatio
            else:
                aspectMode = QtCore.Qt.IgnoreAspectRatio
            show = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = show.shape
            bytesPerLine = 3 * width
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                     bytesPerLine, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(showImage)

            # Add these lines to use high-quality scaling
            size = label_display.size()  # get the size of the label display
            pixmap = pixmap.scaled(size, aspectMode, QtCore.Qt.SmoothTransformation)  # scale the pixmap

            label_display.setPixmap(pixmap)
            label_display.setScaledContents(True)

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
        screen = QGuiApplication.primaryScreen().geometry()  # Get screen size
        size = self.geometry()  # Get current window size
        # Move window to center of screen
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def mousePressEvent(self, event):
        """
        Event handler for mouse press event.

        :param event: The mouse event.
        """
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        """
        Event handler for mouse move event.

        :param QMouseEvent: The mouse event.
        """
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)
                QMouseEvent.accept()
        except:
            pass

    def mouseReleaseEvent(self, QMouseEvent):
        """
        Event handler for mouse release event.

        :param QMouseEvent: The mouse event.
        """
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

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
            width = label.width() if width is None else width  # 宽度
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
            width = label.width() if width is None else width  # 宽度
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
            width = label.width() if width is None else width  # 宽度
            height = label.height() if height is None else height

            pixmap = verticalBar(label_name, value, colors, width, height,
                                 color_text=color_text, alpha=alpha, margin=margin)
            label.setPixmap(pixmap)
            label.setScaledContents(True)


class FLoginDialog(QDialog):
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
        pass

    def setUiStyle(self, windowFlag=False, transBackFlag=False):
        """
        Sets the user interface style and widget states of the dialog.

        :param windowFlag: If True, removes the border of the dialog.
        :param transBackFlag: If True, makes the dialog's background transparent.
        """
        if windowFlag:
            self.setWindowFlags(Qt.FramelessWindowHint)  # Removes the border of the dialog
        if transBackFlag:
            self.setAttribute(Qt.WA_TranslucentBackground)  # Makes the dialog's background transparent

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
        if characters is None:
            characters = string.digits + string.ascii_uppercase

        # Generate a random string of given length from the character set
        random_str = ''.join([random.choice(characters) for _ in range(length)])
        self.ver_code = random_str

        # Generate an image for the verification code
        generator = ImageCaptcha(width=width, height=height)
        img = generator.generate_image(random_str)

        # Convert the image to QPixmap
        im = img.convert("RGB")
        data = im.tobytes("raw", "RGB")
        bytesPerLine = 3 * im.size[0]
        qim = QImage(data, im.size[0], im.size[1], bytesPerLine, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qim)

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
        for i in range(len(widgets) - 1):
            self.setTabOrder(widgets[i], widgets[i + 1])  # Set the tab order for the pair of widgets

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
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # Get the position of the mouse relative to the window
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # Change mouse icon to OpenHandCursor

    def mouseMoveEvent(self, QMouseEvent):
        """
        Overriding the mouseMoveEvent for custom behavior.

        :param QMouseEvent: The mouse move event.
        """
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # Change the window position
                QMouseEvent.accept()
        except:
            pass

    def mouseReleaseEvent(self, QMouseEvent):
        """
        Overriding the mouseReleaseEvent for custom behavior.

        :param QMouseEvent: The mouse release event.
        """
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))  # Change mouse icon to ArrowCursor
