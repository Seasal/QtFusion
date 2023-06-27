style_norm = """
/* General settings for all widgets */
QWidget {
    background-color: #333;
    color: #EEE;
    font-size: 16px;
    border-radius: 5px;
}

/* Tool Button */
QToolButton {
    background-color: #555;
    color: #EEE;
    border: none;
    padding: 3px;
    border-radius: 5px;
}

QToolButton:hover {
    background-color: #777;
}

QToolButton:pressed {
    background-color: #999;
}

/* Table Widget */
QTableWidget {
    border-style: solid;
    border-width: 1px;
    border-color: #555;
    border-radius: 0px;
    background-color: #333;
    color: #EEE;
    gridline-color: #555;
    outline: none;
}

QTableWidget QHeaderView::section {
    background-color: #555;
    color: #EEE;
    padding: 5px;
    border: 1px solid #777;
}

QTableWidget QTableCornerButton::section {
    background-color: #555;
    color: #EEE;
}

QTableWidget::item {
    background-color: #333;
    color: #EEE;
}

QTableWidget::item:selected {
    background-color: #777;
}


/* Push Button */
QPushButton {
    background-color: #555;
    color: #EEE;
    border: none;
    padding: 5px;

}

QPushButton:hover {
    background-color: #777;
}

QPushButton:pressed {
    background-color: #999;
}

/* Line Edit */
QLineEdit {
    background-color: #555;
    color: #EEE;
    border: none;
    padding: 5px;
}

/* Black Theme for QTextEdit */
QTextEdit {
    background-color: #333;
    color: #EEE;
    border: 1px solid #555;
    padding: 0px;
}

QTextEdit QScrollBar:vertical {
    width: 1px;
    height: 1px
}

QTextEdit QScrollBar::handle:vertical {
    background: gray;
}

QTextEdit QScrollBar::add-line:vertical, QTextEdit QScrollBar::sub-line:vertical {
    width: 0px;
    height: 0px;
}

QTextEdit:focus {
    border: 1px solid #777;
}

/* Label */
QLabel {
    color: #EEE;
    font-size: 18px;
    font-family: 'Arial';
}

/* Scroll Bar */
QScrollBar:vertical {
    width: 8px;
    background-color: #555;
}

QScrollBar::handle:vertical {
    background-color: #777;
    min-height: 20px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    height: 8px;
    background-color: #555;
}

QScrollBar::handle:horizontal {
    background-color: #777;
    min-width: 20px;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Combo Box */
QComboBox {
    background-color: #555;
    color: #EEE;
    border: none;
    padding: 5px;
    font: italic 12pt "Consolas";
}

QComboBox:editable {
    background-color: #555;
}

QComboBox QAbstractItemView {
    color: #EEE;
    background-color: #555;
    selection-background-color: #777;
}

/* Spin Box */
QSpinBox {
    background-color: #555;
    color: #EEE;
    border: none;
    padding: 5px;
}

/* Slider */
QSlider::groove:horizontal {
    background-color: #555;
    height: 5px;
}

QSlider::handle:horizontal {
    background-color: #777;
    width: 15px;
    margin: -5px 0;
}

QSlider::groove:vertical {
    background-color: #555;
    width: 5px;
}

QSlider::handle:vertical {
    background-color: #777;
    height: 15px;
    margin: 0 -5px;
}

/* Radio Button */
QRadioButton {
    color: #EEE;
    padding: 5px;
}

QRadioButton::indicator {
    width: 15px;
    height: 15px;
}

QRadioButton::indicator::unchecked {
    image: url(":/default_icons/radio_unchecked.png");
}

QRadioButton::indicator::checked {
    image: url(":/default_icons/radio_checked.png");
}

/* Check Box */
QCheckBox {
    color: #EEE;
    padding: 5px;
}

QCheckBox::indicator {
    width: 15px;
    height: 15px;
}

QCheckBox::indicator::unchecked {
    image: url(":/default_icons/check_unchecked.png");
}

QCheckBox::indicator::checked {
    image: url(":/default_icons/check_checked.png");
}

/* Progress Bar */
QProgressBar {
    background-color: #555;
    color: #EEE;
    border: none;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #777;
}

/* Menu and Menu Bar */
QMenuBar {
    background-color: #555;
}

QMenuBar::item {
    color: #EEE;
}

QMenuBar::item:selected {
    background-color: #777;
}

QMenu {
    background-color: #555;
}

QMenu::item {
    color: #EEE;
}

QMenu::item:selected {
    background-color: #777;
}

/* Tool Tip */
QToolTip {
    background-color: #777;
    color: #EEE;
    border: none;
}
"""
