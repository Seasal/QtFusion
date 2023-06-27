# QtFusion, AGPL-3.0 license
"""
QtFusion is a Python library created by Seasal Wesley (seasalwesley@gmail.com) for
the convenient creation of PySide6 applications that interact with deep learning models.
It provides user interface management and beautification, database management,
image/video/camera processing, model interface definition, and event handling.
This makes it easy for users to create deep learning applications.

Python Version Required: 3.8
Dependencies: numpy, opencv-python>=4.5.5.64, Pillow>=9.0.1, PySide6>=6.4.2, PyYAML>=6.0, captcha>=0.4
"""

import sys
import pkg_resources
import os
import tempfile
from PIL import ImageFont
from PySide6.QtCore import QFile, QIODevice
import warnings
from . import RecSystem

# Check Python version
if not sys.version_info >= (3, 8):
    warnings.warn("Python 3.8 or above is recommended.")

# Check other dependencies
required_packages = {
    "numpy": "",  # no specific version requirement
    "opencv-python": "4.5.5.64",
    "Pillow": "9.0.1",
    "PySide6": "6.4.2",
    "PyYAML": "6.0",
    "captcha": "0.4"
}

for package, required_version in required_packages.items():
    try:
        pkg_resources.get_distribution(package)
        if required_version:
            actual_version = pkg_resources.get_distribution(package).version
            if pkg_resources.parse_version(actual_version) < pkg_resources.parse_version(required_version):
                warnings.warn(
                    f"{package} {required_version} or above is recommended, but {actual_version} is installed.")
    except pkg_resources.DistributionNotFound:
        warnings.warn(f"{package} is recommended but is not installed.")

# Get current script path
current_dir = os.path.dirname(os.path.realpath(__file__))

# Use os.path.join to join paths
font_path = os.path.join(current_dir, '楷体_GB2312.ttf')

try:
    fontC = ImageFont.truetype(font_path, 24)  # Set display font
    fontB = ImageFont.truetype(font_path, 18)
except IOError:
    # If loading font from file system fails, try to load font from Qt resource system
    qfile = QFile(":/楷体_GB2312.ttf")
    qfile.open(QIODevice.ReadOnly)
    data = qfile.readAll().data()  # Get byte data

    try:
        # Create a temporary file
        temp_path = os.path.join(tempfile.gettempdir(), "temp_font.ttf")

        # Write font data into temporary file
        with open(temp_path, "wb") as f:
            f.write(data)
    except Exception as e:
        raise IOError("Unable to write font to temporary file: " + str(e))

    try:
        # Use Pillow to read font from temporary file
        fontC = ImageFont.truetype(temp_path, 24)
        fontB = ImageFont.truetype(temp_path, 18)
    except Exception as e:
        raise IOError("Unable to load font from temporary file: " + str(e))

__version__ = '0.1'
__author__ = 'Seasal Wesley'
__email__ = 'seasalwesley@gmail.com'
__license__ = 'AGPL-3.0'
__url__ = 'https://github.com/seasal/QtFusion'
