# QtFusion, AGPL-3.0 license
import os
from .BaseFrame import loadQssStyles

from .qss.style_trans_black import Trans
from .qss.style_login_white import login_trans
from .qss.style_norm_black import style_norm
from .qss.style_norm_white import white_theme_style


class BaseStyle:
    """
    This class serves as a style decorator to apply custom styles to Qt widgets.
    It supports using either predefined style names or custom QSS files.
    """

    # Define a dictionary that maps style names to their style constants.
    _styles = {
        'STYLE_TRANS': Trans,
        'STYLE_LOGIN': login_trans,
        'STYLE_NORM': style_norm,
        'NORM_WHITE': white_theme_style
    }

    def __init__(self, style_name_or_const='STYLE_TRANS'):
        """
        Initialize the style decorator with a default or given style.

        Arguments:
            style_name_or_const: Either a predefined style name or a QSS file.
            Defaults to 'STYLE_TRANS' if not specified.
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

    def set_named_style(self, widget, style_name):
        """
        Apply a predefined style to a given widget.

        Arguments:
            widget: The widget to apply the style to.
            style_name: The name of the style to apply.
        """

        if isinstance(style_name, str):
            if style_name in self._styles:
                widget.setStyleSheet(self._styles[style_name])
            elif os.path.isfile(style_name):
                with open(style_name, 'r') as f:
                    widget.setStyleSheet(f.read())
            else:
                raise ValueError(f'Invalid input: {style_name}')
        else:
            raise TypeError(f'Invalid input type: {type(style_name).__name__}')

    def set_style_text(self, widget, style_text):
        """
        Apply a given style text to a widget.

        Arguments:
            widget: The widget to apply the style to.
            style_text: The style text to apply.
        """
        widget.setStyleSheet(style_text)
