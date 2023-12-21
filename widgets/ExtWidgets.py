# QtFusion, AGPL-3.0 license
import cv2
from IMcore.IMextension import IMageLabel, IMessageBox, IMExtWindow
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QToolButton, QMessageBox, QApplication, QPushButton, QDialog

from .. import __package_name__
from ..config.QfConfig import QF_Config

AVATAR = ":/default_icons/default_avatar.png"
HOME = ":/default_icons/home.png"
BIG_SIZE = ":/default_icons/bigsize.png"
SMALL_SIZE = ":/default_icons/smallsize.png"


class FImageLabel(IMageLabel):
    """
    A QLabel extension that provides additional functionality for displaying images.

    This class extends QLabel, providing the ability to display images and text. It allows for interactive
    manipulation of the image being displayed. This includes the ability to scale the image in and out using the mouse
    wheel (zooming), as well as panning the image by clicking and dragging with the mouse.

    The class also provides a set of buttons for image scaling: resetting to the original size, and increasing or
    decreasing the size by 10%.
    """

    def __init__(self, parent=None, *args, **kwargs):
        """
        Initializes the FImageLabel instance.

        :param parent: The parent widget to the label. Default is None.
        """
        super(FImageLabel, self).__init__(parent, *args, **kwargs)
        self.init_ui()  # Initialize UI

    def setAspectMode(self, keepAspect: bool):
        """
        Sets the aspect ratio mode for the label.

        :param keepAspect: If True, the aspect ratio is maintained.
        """
        super().setAspectMode(keepAspect)

    def init_ui(self):
        """
        Initializes the user interface (UI) of the label.
        """

        self.setWindowTitle("ImageBox")
        self.setStyleSheet("QFrame{border:1px solid #44cef6;\n"
                           "background-color: transparent;}")
        self.boxToolButton()  # Initialize the toolbar buttons

    def dispImage(self, image, keepAspect=True):
        """
        Displays an image read by OpenCV in the label.

        :param image: The image to display.
        :param keepAspect: If True, the aspect ratio of the image is maintained.
        """
        show = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert the image to RGB
        super().dispImage(show, keepAspect)

    def dispText(self, text):
        """
        Displays text in the label.

        :param text: The text to display.
        """
        super().dispText(text)

    def paintEvent(self, e):
        """
        Handles paint events.

        :param e: The paint event.
        """
        super().paintEvent(e)

    def wheelEvent(self, event):
        """
        Handles mouse wheel events. This will allow to zoom the image in or out.

        :param event: The wheel event.
        """
        super().wheelEvent(event)

    def mouseMoveEvent(self, e):
        """
        Handles mouse move events. This will allow to pan the image when the mouse is moved.

        :param e: The mouse event.
        """
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e):
        """
        Handles mouse press events. This will start the panning operation.

        :param e: The mouse event.
        """
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """
        Handles mouse release events. This will end the panning operation.

        :param e: The mouse event.
        """
        super().mouseReleaseEvent(e)

    def boxToolButton(self, button_size=25):
        """
        Sets up the buttons for the tool bar.

        :param button_size: The size of the buttons.
        """

        button_normal = QToolButton(self)
        button_normal.move(self.geometry().x(), self.geometry().y())
        button_normal.setFixedSize(button_size, button_size)
        button_normal.setStyleSheet("""QToolButton{background-color: transparent;border-image: none;}
                                    QToolButton::hover{border: 0px;} """)
        icon = QtGui.QIcon()
        icon.addPixmap(QPixmap(HOME), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button_normal.setIcon(icon)
        button_normal.setIconSize(QtCore.QSize(button_size, button_size))
        button_normal.clicked.connect(self.normButton)

        button_bigger = QToolButton(self)
        pos = self.geometry().x() + button_size + 10, self.geometry().y()
        button_bigger.move(pos[0], pos[1])
        button_bigger.setFixedSize(button_size, button_size)
        button_bigger.setStyleSheet("""QToolButton{background-color: transparent;border-image: none;}
                                        QToolButton::hover{border: 0px;} """)
        icon = QtGui.QIcon()
        icon.addPixmap(QPixmap(BIG_SIZE), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button_bigger.setIcon(icon)
        button_bigger.setIconSize(QtCore.QSize(button_size, button_size))
        button_bigger.clicked.connect(self.bigButton)

        button_smaller = QToolButton(self)
        button_smaller.move(pos[0] + button_size + 10, pos[1])
        button_smaller.setFixedSize(button_size, button_size)
        button_smaller.setStyleSheet("""QToolButton{background-color: transparent;border-image: none;}
                                       QToolButton::hover{border: 0px;} """)
        icon = QtGui.QIcon()
        icon.addPixmap(QPixmap(SMALL_SIZE), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button_smaller.setIcon(icon)
        button_smaller.setIconSize(QtCore.QSize(button_size, button_size))
        button_smaller.clicked.connect(self.smallButton)

    def normButton(self):
        """
        Resets the image size to the original size.
        """
        super().normButton()

    def bigButton(self):
        """
        Increases the size of the image by 10%.
        """
        super().bigButton()

    def smallButton(self):
        """
        Decreases the size of the image by 10%.
        """
        super().smallButton()


class FWindowCtrls(IMExtWindow):
    """
    This class represents a main window with custom controls, including close, minimize, and hint buttons.
    Inherits from QMainWindow.
    """

    def __init__(self, main_window, exit_title, exit_message, icon=AVATAR,
                 button_sizes=(20, 20),
                 button_gaps=30, button_right_margin=80, hint_flag=False):
        """
        Initializes the FWindowCtrls instance.

        :param main_window: Reference to the main window.
        :param exit_title: The title for the exit message box.
        :param exit_message: The message for the exit message box.
        :param icon: The default icon for the window.
        :param button_sizes: Tuple representing the sizes of the buttons.
        :param button_gaps: The gaps between the buttons.
        :param button_right_margin: The right margin for the buttons.
        :param hint_flag: Flag to control hint visibility.
        """

        super().__init__(main_window)
        self.verbose = QF_Config.VERBOSE
        self.msg_box = None  # Message box instance
        self.main_window = main_window  # Reference to the main window
        self.hint_flag = hint_flag  # Flag to control hint visibility
        self.exit_title = exit_title  # Exit message box title
        self.exit_message = exit_message  # Exit message box message
        self.icon = icon  # Default icon for the window
        self.button_right_margin = button_right_margin  # Right margin for the buttons
        self.button_gaps = button_gaps  # Gaps between buttons
        self.button_sizes = button_sizes  # Sizes of buttons
        self.setupWindowControls()  # Initialize window controls

    def closeQButton(self):
        """
        Method to create a QMessageBox on closing the application.
        """
        reply = QMessageBox.question(self.main_window, self.exit_title, self.exit_message,
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event = QApplication.instance()
            event.quit()  # Quit the application
            if self.verbose:
                print(f"{__package_name__} Closed...")
            else:
                print("Closed...")
        else:
            return

    def setMessageBox(self, title="Message Box", message="Are you sure you want to quit?", yes_text="Yes", no_text="No",
                      hint_flag=False, icon=HOME):
        """
        Method to set a custom message box.

        :param title: The title of the message box.
        :param message: The message in the message box.
        :param yes_text: The text for the Yes button.
        :param no_text: The text for the No button.
        :param hint_flag: Flag for hint visibility.
        :param icon: Icon for the message box.
        """
        self.msg_box = FMessageBox(title=title, message=message, yes_text=yes_text, no_text=no_text,
                                   hint_flag=hint_flag)
        self.msg_box.set_icon(icon)  # Set the icon for the message box

    def closeButton(self):
        """
        Method to handle the close button event.
        """
        if self.msg_box is None:
            self.msg_box = FMessageBox(title=self.exit_title, message=self.exit_message, hint_flag=self.hint_flag)
            self.msg_box.set_icon(self.icon)

        # Ensure that the size of the message box is set
        self.msg_box.adjustSize()

        # Get the geometry of the main window and the message box
        mw_frame = self.main_window.frameGeometry()
        msg_box_frame = self.msg_box.frameGeometry()

        # Calculate and set the position of the message box
        center_point = mw_frame.center() - QPoint(msg_box_frame.width() / 2, msg_box_frame.height() / 2)
        self.msg_box.move(center_point)

        reply = self.msg_box.result()
        if reply == QDialog.Accepted:
            event = QApplication.instance()
            event.quit()  # Quit the application
            if self.verbose:
                print(f"{__package_name__} Closed...")
            else:
                print("Closed...")
        else:
            return

    def minButton(self):
        """
        Method to minimize the main window.
        """
        self.main_window.showMinimized()

    def hintButton(self):
        """
        Method to handle the hint button event.
        """
        if self.hint_flag:
            pass  # Code to handle hint flag being True
        else:
            pass  # Code to handle hint flag being False
        self.hint_flag = not self.hint_flag  # Toggle the hint flag

    def setupWindowControls(self):
        """
        Method to set up window controls like buttons.
        """
        # Code for setting up and displaying the close button
        pos_x = self.main_window.size().width()
        button_red = QPushButton(self.main_window)
        button_red.move(pos_x - self.button_right_margin, 20)
        button_red.setFixedSize(self.button_sizes[0], self.button_sizes[1])
        button_red.setStyleSheet("QPushButton{\n"
                                 "    background:#CE0000;\n"
                                 "    color:white;\n"
                                 "    box-shadow: 1px 1px 3px;border-radius: 10px;\n"
                                 "}\n"
                                 "QPushButton:hover{                    \n"
                                 "    background:red;\n"
                                 "}\n"
                                 "QPushButton:pressed{\n"
                                 "    border: 1px solid #3C3C3C!important;\n"
                                 "    background:black;\n"
                                 "}")
        button_red.setToolTip("Close")
        button_red.clicked.connect(self.closeButton)  # Connect the close button event

        button_orange = QPushButton(self.main_window)
        button_orange.move(pos_x - self.button_right_margin - self.button_gaps, 20)
        button_orange.setFixedSize(self.button_sizes[0], self.button_sizes[1])
        button_orange.setStyleSheet("QPushButton{\n"
                                    "    background:orange;\n"
                                    "    color:white;\n"
                                    "    box-shadow: 1px 1px 3px;border-radius: 10px;\n"
                                    "}\n"
                                    "QPushButton:hover{                    \n"
                                    "    background:yellow;\n"
                                    "}\n"
                                    "QPushButton:pressed{\n"
                                    "    border: 1px solid #3C3C3C!important;\n"
                                    "    background:black;\n"
                                    "}")
        button_orange.setToolTip("No response when clicked")
        button_orange.clicked.connect(self.hintButton)

        button_green = QPushButton(self.main_window)
        button_green.move(pos_x - self.button_right_margin - 2 * self.button_gaps, 20)
        button_green.setFixedSize(self.button_sizes[0], self.button_sizes[1])
        button_green.setStyleSheet("QPushButton{\n"
                                   "    background:green;\n"
                                   "    color:white;\n"
                                   "    box-shadow: 1px 1px 3px;border-radius: 10px;\n"
                                   "}\n"
                                   "QPushButton:hover{                    \n"
                                   "    background:#08BF14;\n"
                                   "}\n"
                                   "QPushButton:pressed{\n"
                                   "    border: 1px solid #3C3C3C!important;\n"
                                   "    background:black;\n"
                                   "}")
        button_green.setToolTip("Minimize")
        button_green.clicked.connect(self.minButton)


class FMessageBox(IMessageBox):
    """
    This class represents a custom message box that inherits from QDialog.
    The message box includes a title, a message, and Yes/No buttons.
    """

    def __init__(self, title="Message Box", message="", yes_text="Yes", no_text="No", hint_flag=True, parent=None):
        """
        Initializes the FMessageBox instance.

        :param title: The title of the message box.
        :param message: The message to display.
        :param yes_text: The text for the Yes button.
        :param no_text: The text for the No button.
        :param hint_flag: Flag to control frame visibility.
        :param parent: The parent widget.
        """
        super(FMessageBox, self).__init__(parent)

        self.setWindowTitle(title)  # Set the title of the message box

        if hint_flag:
            self.setWindowFlags(Qt.FramelessWindowHint)  # Removes the window frame if hint_flag is True

        self.layoutMessage(message, yes_text, no_text)

        # Apply the default QSS stylesheet
        self.set_stylesheet()

        # Connect the button clicked signals to the appropriate slots
        self.yes_button.clicked.connect(self.accept)
        self.no_button.clicked.connect(self.reject)

    def set_message(self, message):
        """
        Sets the message in the message box.

        :param message: The message to set.
        """
        self.message.setText(message)

    def set_icon(self, icon_path):
        """
        Sets the window icon.

        :param icon_path: The path to the icon file.
        """
        super().set_icon(icon_path)

    def result(self):
        """
        Executes the QDialog and returns the result.
        """
        return self.exec_()

    def set_stylesheet(self, stylesheet=None):
        """
        Sets the QSS stylesheet.

        :param stylesheet: The QSS stylesheet to apply. If None, the default stylesheet is used.
        """
        if stylesheet is None:
            stylesheet = """
                MessageBox {
                    background-color: rgba(255, 255, 255, 0.4);
                    border-radius: 10px;
                }
                QLabel {
                    color: black;
                    font-size: 20px;
                    text-align: center;
                }
                QPushButton {
                    color: #F0F0F0;
                    font-size: 20px;
                    background-color: #1E90FF;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #3BB9FF;
                }
                QPushButton:pressed {
                    background-color: #1569C7;
                }
            """
        self.setStyleSheet(stylesheet)  # Apply the stylesheet
