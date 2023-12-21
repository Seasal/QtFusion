import logging
import os
import yaml
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QMainWindow, QWidget
from IMcore.IMsets import loadSettings

from ..path import abs_path, path_exists
logger = logging.getLogger(__name__)


def applyText(widget, text):
    """
    Apply text settings to a widget.

    Args:
        widget (QWidget or QLabel): Widget to apply the text to.
        text (str): Text to be applied.
    """
    widget.setText(text)


def applyIcon(widget, icon_path):
    """
    Apply icon settings to a widget.

    Args:
        widget (QWidget or ): Widget to apply the icon to.
        icon_path (str): Path to the icon file.
    """
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_path), QIcon.Mode.Normal, QIcon.State.Off)
    widget.setIcon(icon)


def applyBackground(widget, background_path):
    """
    Apply background settings to a widget.

    Args:
        widget (QWidget or object): Widget to apply the background to.
        background_path (str): Path to the background file.
    """
    widget.setStyleSheet(f"border-image: url({background_path})")


def loadYamlSettings(window, yaml_file, base_path="./"):
    """
    Load settings for a QWidget from a YAML file and apply them to the specified window.

    Args:
        window (QMainWindow or QWidget): The main window where the settings will be applied.
        yaml_file (str): The file path of the YAML file containing the settings.
        base_path (str, optional): The base path used for resolving relative paths. Default is None.

    The function iterates over each setting in the YAML file, finds the corresponding widget in the window,
    and applies the settings like text, icon, background, and window icon. It uses the 'abs_path' function
    to resolve the absolute path of the resources and 'path_exists' to check the existence of these paths.
    """
    from ..widgets.Widgets import QImageLabel
    try:
        with open(yaml_file, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)
    except Exception as e:
        raise RuntimeError(f"Error loading YAML file '{yaml_file}': {e}")

    for widget_name, settings in yaml_data.items():
        try:
            widget_type = eval(settings['type'])
            widget = window.findChild(widget_type, widget_name)
            loadSettings(window, widget, widget_name, settings, base_path)
        except KeyError as e:
            print(f"Key error in yaml data '{yaml_file}': {widget_name} has no key {e}")
        except NameError as e:
            print(f"Name error in '{yaml_file}': {e}")
        except AttributeError as e:
            print(f"Attribute error in finding widget for '{yaml_file}': {e}")
        except Exception as e:
            print(f"Unexpected error in '{yaml_file}': {e}")


def apply_WindowIcon(window, settings, base_path):
    """
    Apply window icon setting to the main window.

    Args:
        window (QMainWindow): Main window to which the window icon is applied.
        settings (dict): Dictionary containing the window icon setting.
        base_path (str): Base path for resolving relative paths.
    """
    window_icon_path = abs_path(base_path=base_path, relative_path=settings['windowIcon'])
    if path_exists(window_icon_path):
        icon = QIcon()
        icon.addPixmap(QPixmap(window_icon_path), QIcon.Mode.Normal, QIcon.State.Off)
        window.setWindowIcon(icon)
    else:
        logging.warning(f"Window icon file not found at '{window_icon_path}'")


def applyWindowIcon(window, icon_path):
    """
    Apply window icon settings to a window.

    Args:
        window (QMainWindow or QWidget): Window to apply the icon to.
        icon_path (str): Path to the window icon file.
    """
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_path), QIcon.Mode.Normal, QIcon.State.Off)
    window.setWindowIcon(icon)


def applyQssStyles(window, qss_data):
    """
    Apply QSS styles to a QMainWindow.

    Args:
        window (QMainWindow or ): The window to apply the styles to.
        qss_data (str): The QSS styles to be applied.
    """
    window.setStyleSheet(qss_data)


def applyWidgetSettings(widget, widget_name, settings, base_path):
    """
    Apply individual settings to a widget.

    Args:
        widget_name (str): Widget name to which settings are applied.
        widget (QWidget or): Widget to which settings are applied.
        settings (dict): Dictionary of settings for the widget.
        base_path (str): Base path for resolving relative paths.
    """
    if 'text' in settings:
        applyText(widget, settings['text'])

    if 'icon' in settings:
        icon_path = abs_path(base_path=base_path, relative_path=settings['icon'])
        if path_exists(icon_path):
            applyIcon(widget, icon_path)
        else:
            logging.warning(f"Icon file not found at '{icon_path}'")

    if 'background' in settings:
        background_path = abs_path(base_path=base_path, relative_path=settings['background'])
        if path_exists(background_path):
            widget.setStyleSheet(f"#{widget_name} {{ border-image: url({background_path}) }}")
            applyBackground(widget, background_path)
        else:
            logging.warning(f"Background file not found at '{background_path}'")
