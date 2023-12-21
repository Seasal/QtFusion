# QtFusion, AGPL-3.0 license
from PySide6.QtWidgets import QLabel

from .BaseFrame import FBaseWindow, dispImage, FLoginDialog
from .ExtWidgets import *
from ..styles import loadQssStyles, loadYamlSettings, BaseStyle


class QMainWindow(FBaseWindow):
    """
    QMainWindow is a class derived from QMainWindow to provide custom methods
    and properties for handling graphical user interface (GUI) related operations
    in the application.
    """

    def __init__(self, parent=None, *args, **kwargs):
        """
        Initializes the QMainWindow instance.

        :param parent: Parent QWidget. Defaults to None.
        """
        super(QMainWindow, self).__init__(parent, *args, **kwargs)
        QLabel.dispImage = dispImage
        self.styles = BaseStyle()

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

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)

    def setNamedStyle(self, style_name='STYLE_TRANS'):
        """
        Apply a predefined style to the widget.

        Args:
            style_name (str): The name of the predefined style to apply. Available styles are:
                - 'STYLE_TRANS': Black transition style.
                - 'STYLE_LOGIN': White login style.
                - 'STYLE_NORM': Black normal style.
                - 'NORM_WHITE': White normal style.
                - 'NORM_GREEN': Green main style.
                - 'NormDark': Dark style.
                - 'MacOS': MacOS style.
                - 'Ubuntu': Ubuntu style.
                - 'ElegantDark': Elegant dark style.
                - 'Aqua': Aqua style.
                - 'NeonButtons': Neon buttons style.
                - 'NeonBlack': Neon black style.
                - 'BlueGlass': Blue glass style.
                - 'Dracula': Dracula (dark) style.
                - 'NightEyes': Night eyes style.
                - 'Parchment': Parchment style.
                - 'DarkVs15': Dark Visual Studio 2015 style.
                - 'DarkGreen': Dark green style.
                - 'DarkOrange': Dark orange style.
                - 'DarkPink': Dark pink style.
                - 'DarkPurple': Dark purple style.
                - 'DarkRed': Dark red style.
                - 'DarkYellow': Dark yellow style.
                - 'Skyrim': Skyrim style.
                - 'LightStyle': Light style.

        Raises:
            TypeError: If the style name is not a string.
            ValueError: If the style name is not found in predefined styles and is not a valid file path.
        """
        self.styles.set_named_style(self, style_name)

    def setStyleText(self, style_text):
        """
        Apply a given style text to a widget.

        Args:
            style_text: The style text to apply.
        """
        self.styles.set_style_text(self, style_text)

    def loadYamlSettings(self, yaml_file, base_path="./"):
        """
        Load settings for a QWidget from a YAML file and apply them to the specified window.

        Args:
            yaml_file (str): The file path of the YAML file containing the settings.
            base_path (str, optional): The base path used for resolving relative paths. Default is None.
        """
        loadYamlSettings(self, yaml_file, base_path)


class QLoginDialog(FLoginDialog):
    """
    A custom QDialog class representing a Login Dialog in a GUI application. This class inherits from QDialog.
    """

    def __init__(self, parent=None, *args, **kwargs):
        super(QLoginDialog, self).__init__(parent, *args, **kwargs)
        self.styles = BaseStyle()

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)

    def loadYamlSettings(self, yaml_file, base_path="./"):
        """
        Load settings for a QWidget from a YAML file and apply them to the specified window.

        Args:
            yaml_file (str): The file path of the YAML file containing the settings.
            base_path (str, optional): The base path used for resolving relative paths. Default is None.
        """
        loadYamlSettings(self, yaml_file, base_path)

    def setNamedStyle(self, style_name='STYLE_TRANS'):
        """
        Apply a predefined style to the widget.

        Args:
            style_name (str): The name of the predefined style to apply. Available styles are:
                - 'STYLE_TRANS': Black transition style.
                - 'STYLE_LOGIN': White login style.
                - 'STYLE_NORM': Black normal style.
                - 'NORM_WHITE': White normal style.
                - 'NORM_GREEN': Green main style.
                - 'NormDark': Dark style.
                - 'MacOS': MacOS style.
                - 'Ubuntu': Ubuntu style.
                - 'ElegantDark': Elegant dark style.
                - 'Aqua': Aqua style.
                - 'NeonButtons': Neon buttons style.
                - 'NeonBlack': Neon black style.
                - 'BlueGlass': Blue glass style.
                - 'Dracula': Dracula (dark) style.
                - 'NightEyes': Night eyes style.
                - 'Parchment': Parchment style.
                - 'DarkVs15': Dark Visual Studio 2015 style.
                - 'DarkGreen': Dark green style.
                - 'DarkOrange': Dark orange style.
                - 'DarkPink': Dark pink style.
                - 'DarkPurple': Dark purple style.
                - 'DarkRed': Dark red style.
                - 'DarkYellow': Dark yellow style.
                - 'Skyrim': Skyrim style.
                - 'LightStyle': Light style.

        Raises:
            TypeError: If the style name is not a string.
            ValueError: If the style name is not found in predefined styles and is not a valid file path.
        """
        self.styles.set_named_style(self, style_name)

    def setStyleText(self, style_text):
        """
        Apply a given style text to a widget.

        Args:
            style_text: The style text to apply.
        """
        self.styles.set_style_text(self, style_text)


class QImageLabel(FImageLabel):
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
        Initializes the QImageLabel instance.

        :param parent: The parent widget to the label. Default is None.
        """
        super(QImageLabel, self).__init__(parent, *args, **kwargs)

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)


class QWindowCtrls(FWindowCtrls):
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

        super(QWindowCtrls, self).__init__(main_window, exit_title, exit_message, icon=icon, button_sizes=button_sizes,
                                           button_gaps=button_gaps, button_right_margin=button_right_margin,
                                           hint_flag=hint_flag)

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)


class QMessageBox(FMessageBox):
    """
    This class represents a custom message box that inherits from QDialog.
    The message box includes a title, a message, and Yes/No buttons.
    """

    def __init__(self, title="Message Box", message="", yes_text="Yes", no_text="No", hint_flag=True, parent=None):
        """
        Initializes the QMessageBox instance.

        :param title: The title of the message box.
        :param message: The message to display.
        :param yes_text: The text for the Yes button.
        :param no_text: The text for the No button.
        :param hint_flag: Flag to control frame visibility.
        :param parent: The parent widget.
        """
        super(QMessageBox, self).__init__(title=title, message=message, yes_text=yes_text, no_text=no_text,
                                          hint_flag=hint_flag, parent=parent)
        self.styles = BaseStyle()

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)

    def setNamedStyle(self, style_name='STYLE_TRANS'):
        """
        Apply a predefined style to the widget.

        Args:
            style_name (str): The name of the predefined style to apply. Available styles are:
                - 'STYLE_TRANS': Black transition style.
                - 'STYLE_LOGIN': White login style.
                - 'STYLE_NORM': Black normal style.
                - 'NORM_WHITE': White normal style.
                - 'NORM_GREEN': Green main style.
                - 'NormDark': Dark style.
                - 'MacOS': MacOS style.
                - 'Ubuntu': Ubuntu style.
                - 'ElegantDark': Elegant dark style.
                - 'Aqua': Aqua style.
                - 'NeonButtons': Neon buttons style.
                - 'NeonBlack': Neon black style.
                - 'BlueGlass': Blue glass style.
                - 'Dracula': Dracula (dark) style.
                - 'NightEyes': Night eyes style.
                - 'Parchment': Parchment style.
                - 'DarkVs15': Dark Visual Studio 2015 style.
                - 'DarkGreen': Dark green style.
                - 'DarkOrange': Dark orange style.
                - 'DarkPink': Dark pink style.
                - 'DarkPurple': Dark purple style.
                - 'DarkRed': Dark red style.
                - 'DarkYellow': Dark yellow style.
                - 'Skyrim': Skyrim style.
                - 'LightStyle': Light style.

        Raises:
            TypeError: If the style name is not a string.
            ValueError: If the style name is not found in predefined styles and is not a valid file path.
        """
        self.styles.set_named_style(self, style_name)

    def setStyleText(self, style_text):
        """
        Apply a given style text to a widget.

        Args:
            style_text: The style text to apply.
        """
        self.styles.set_style_text(self, style_text)
