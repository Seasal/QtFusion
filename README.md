# QtFusion

## Introduction
QtFusion is a versatile Python library for building applications. It focuses on seamlessly integrating deep learning models, offering a suite of tools for UI management, beautification, database management, as well as handling image/video/camera processing, model interface definition, and event handling. This library simplifies the creation of advanced deep learning applications.

## Features
- UI Enhancement: Provides tools for beautifying and managing the user interface. 
- Database Management: Facilitates easy handling of database operations. 
- Media Processing: Supports image, video, and camera data processing. 
- Model Integration: Simplifies the integration of deep learning models with UI. 
- Event Handling: Efficient management of application events.

## Installation
To successfully install QtFusion, follow these guidelines:

1. **Python Version**: Ensure you have Python 3.8 or newer installed, as QtFusion is designed to work best with these versions.
2. **Install Dependencies**: QtFusion relies on several key libraries. Install them using pip:

```bash
pip install numpy
pip install opencv-python>=4.5.5.64
pip install Pillow>=9.0.1
pip install PySide6>=6.4.2
pip install PyYAML>=6.0
pip install IMcore>=0.2.1
```
These commands will install the required versions of numpy, opencv-python, Pillow, PySide6, PyYAML, and captcha.

3. **Deep Learning Libraries**: For deep learning projects, it's recommended to use either PyTorch or TensorFlow. Future versions of QtFusion will support PyQt5, PyQt6, and PySide6.
4. **Install QtFusion**: Finally, install QtFusion:

```bash
pip install QtFusion
```


## Usage
To use QtFusion in your PySide6 project:
* Import FBaseWindow from QtFusion.BaseFrame.
* Define your main window class, inheriting from FBaseWindow.
* Initialize a QApplication, create an instance of your main window, and call necessary methods.
* Start the application with app.exec().

This will allow you to incorporate QtFusion's features into your PySide6 application, enhancing its interface and functionality.

```python
from Your_UI import Ui_MainWindow
from QtFusion import QMainWindow
from PySide6.QtWidgets import QApplication
from sys import argv, exit
class YourMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super(YourMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

app = QApplication(argv)
win = YourMainWindow()
win.showTime()
exit(app.exec()) 
```

This is a basic example to get started. For more advanced features, refer to the QtFusion documentation and examples.


## Acknowledgments
Special thanks to all contributors who have helped in developing QtFusion.

## Contact
For support or queries, please contact [seasalwesley@gmail.com](seasalwesley@gmail.com).
