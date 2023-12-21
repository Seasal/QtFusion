# QtFusion, AGPL-3.0 license
import logging
import os
from IMcore.IMsets import loadStyles

from ..path import get_script_dir, abs_path
from ..utils.FileUtils import readQssFile

logger = logging.getLogger(__name__)


class BaseStyle:
    """
    This class serves as a style decorator to apply custom styles to Qt widgets.
    It supports using either predefined style names or custom QSS files.
    """
    # Define a dictionary that maps style names to their style constants.
    _script_parent_dir = os.path.dirname(get_script_dir())
    _styles = {
        'STYLE_TRANS': abs_path("/qss/style_trans_black.qss", _script_parent_dir),
        'STYLE_LOGIN': abs_path("/qss/style_login_white.qss", _script_parent_dir),
        'STYLE_NORM': abs_path("/qss/style_norm_black.qss", _script_parent_dir),
        'NORM_WHITE': abs_path("/qss/style_norm_white.qss", _script_parent_dir),
        "NORM_GREEN": abs_path("/qss/style_main_green.qss", _script_parent_dir),
        "NormDark": abs_path("/qss/NormDark.qss", _script_parent_dir),
        "MacOS": abs_path("/qss/MacOS.qss", _script_parent_dir),
        "Ubuntu": abs_path("/qss/Ubuntu.qss", _script_parent_dir),
        "ElegantDark": abs_path("/qss/ElegantDark.qss", _script_parent_dir),
        "Aqua": abs_path("/qss/Aqua.qss", _script_parent_dir),
        "NeonButtons": abs_path("/qss/NeonButtons.qss", _script_parent_dir),
        "NeonBlack": abs_path("/qss/NeonBlack.qss", _script_parent_dir),
        "BlueGlass": abs_path("/qss/BlueGlass.qss", _script_parent_dir),
        "Dracula": abs_path("/qss/DarkDracula.qss", _script_parent_dir),
        "NightEyes": abs_path("/qss/NightEyes.qss", _script_parent_dir),
        "Parchment": abs_path("/qss/Parchment.qss", _script_parent_dir),
        "DarkVs15": abs_path("/qss/DarkVs15.qss", _script_parent_dir),
        "DarkGreen": abs_path("/qss/DarkGreen.qss", _script_parent_dir),
        "DarkOrange": abs_path("/qss/DarkOrange.qss", _script_parent_dir),
        "DarkPink": abs_path("/qss/DarkPink.qss", _script_parent_dir),
        "DarkPurple": abs_path("/qss/DarkPurple.qss", _script_parent_dir),
        "DarkRed": abs_path("/qss/DarkRed.qss", _script_parent_dir),
        "DarkYellow": abs_path("/qss/DarkYellow.qss", _script_parent_dir),
        "Skyrim": abs_path("/qss/Skyrim.qss", _script_parent_dir),
        "LightStyle": abs_path("/qss/LightStyle.qss", _script_parent_dir),
    }

    def __init__(self, style_name_or_const='STYLE_TRANS'):
        """
        Initialize the style decorator with either a predefined style name or a QSS file path.
        The default style is 'STYLE_TRANS'.

        Args:
            style_name_or_const (str): The name of the predefined style or a path to a QSS file.
                Defaults to 'STYLE_TRANS'. Available styles are:
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
        """
        self.style_name_or_const = style_name_or_const

    def __new__(cls, style_name_or_const='STYLE_TRANS'):
        """
        Overriding the __new__ method to handle the case where no style is provided.
        In this case, treat the given parameter as a function to be decorated.

        Arguments:
            style_name_or_const: Either a predefined style name or a QSS file, or a function to be decorated.
            Defaults to 'STYLE_TRANS' if not specified.
        """
        # If style_name_or_const is a function, treat it as the function to be decorated.
        if callable(style_name_or_const):
            instance = super().__new__(cls)
            instance.__init__('STYLE_TRANS')  # Initialize the instance with the default style.
            return instance(style_name_or_const)  # Return the decorator function.
        # Otherwise, create a new instance.
        else:
            return super().__new__(cls)

    def __call__(self, func):
        """
        Implement the decorator logic.

        Arguments:
            func: The function to be decorated.
        """

        def wrapped_func(*args, **kwargs):
            # Assume the first argument is the widget to apply the style to.
            widget = args[0]

            # Ensure the widget has a setStyleSheet method.
            if not hasattr(widget, 'setStyleSheet'):
                raise TypeError("The provided object does not support the setStyleSheet method.")

            # Call the original function.
            result = func(*args, **kwargs)

            # Apply the style.
            # If the style is a predefined style name, apply the corresponding style.
            if isinstance(self.style_name_or_const, str):
                if self.style_name_or_const in self._styles:
                    widget.setStyleSheet(self._styles[self.style_name_or_const])
                # If the style is a QSS file, load and apply the QSS file.
                elif os.path.isfile(self.style_name_or_const):
                    loadQssStyles(widget, self.style_name_or_const)
                # Raise an error for invalid style input.
                else:
                    raise ValueError(f'Invalid input: {self.style_name_or_const}')
            else:
                raise TypeError(f'Invalid input type: {type(self.style_name_or_const).__name__}')

            # Return the result of the original function
            return result

        return wrapped_func

    def set_named_style(self, widget, style_name, encoding="utf-8"):
        """
        Apply a predefined style to a given widget.

        Args:
            widget: The widget to which the style will be applied.
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
            encoding (str): The encoding format of the QSS file. Defaults to 'utf-8'.

        Raises:
            TypeError: If the style name is not a string.
            ValueError: If the style name is not found in predefined styles and is not a valid file path.
        """

        if not isinstance(style_name, str):
            raise TypeError(f"Style name must be a string, not {type(style_name).__name__}")

        file_name = self._styles.get(style_name)

        if not file_name and os.path.isfile(style_name):
            file_name = style_name

        if file_name and os.path.isfile(file_name):
            widget.setStyleSheet(readQssFile(file_name, encoding=encoding))
        else:
            raise ValueError(f"Style '{style_name}' not found in predefined styles, and is not a valid file path.")

    def set_style_text(self, widget, style_text):
        """
        Apply a given style text to a widget.

        Args:
            widget: The widget (or any object) to apply the style to. Must have a 'setStyleSheet' method.
            style_text (str): The style text (QSS) to apply to the widget.

        Raises:
            AttributeError: If 'widget' does not have a 'setStyleSheet' method.
            TypeError: If 'style_text' is not a string.
        """
        if not hasattr(widget, 'setStyleSheet'):
            raise AttributeError(f"The 'widget' provided does not have a 'setStyleSheet' method.")

        if not isinstance(style_text, str):
            raise TypeError(f"Expected 'style_text' to be a string, got {type(style_text).__name__} instead.")

        widget.setStyleSheet(style_text)


def loadQssStyles(window, qss_file, base_path="./"):
    """
    Load QSS styles for a QMainWindow.

    :param window: QMainWindow instance to apply the styles to.
    :param qss_file: Path to the QSS file containing styles.
    :param base_path: Base path for the QSS file, defaults to the current directory.
    """
    # Ensure the widget has a setStyleSheet method.
    if not hasattr(window, 'setStyleSheet'):
        raise TypeError("The provided object does not support the setStyleSheet method.")
    loadStyles(window, qss_file, base_path)
