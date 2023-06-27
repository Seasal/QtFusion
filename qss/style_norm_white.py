white_theme_style = """
/* General settings for all widgets */
QWidget {
    background-color: #EEE;
    color: #333;
    border-radius: 5px;
}

/* Push Button */
QPushButton {
    background-color: #DDD;
    color: #333;
    border: 1px solid #CCC;
    padding: 3px;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #CCC;
}

QPushButton:pressed {
    background-color: #BBB;
}

/* Line Edit */
QLineEdit {
    background-color: #FFF;
    color: #333;
    border: 1px solid #CCC;
    padding: 5px;
}

/* White Theme for QTextEdit */
QTextEdit {
    background-color: #EEE;
    color: #333;
    border: 1px solid #CCC;
    padding: 5px;
}

QTextEdit:focus {
    border: 1px solid #999;
}

/* Label */
QLabel {
    color: #333;
    font-size: 18px;
    font-family: "Microsoft YaHei", "SimSun", "SimHei", "KaiTi", "FangSong";
}

/* Scroll Bar */
QScrollBar:vertical {
    width: 8px;
    background-color: #CCC;
}

QScrollBar::handle:vertical {
    background-color: #BBB;
    min-height: 20px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    height: 4px;
    background-color: #CCC;
}

QScrollBar::handle:horizontal {
    background-color: #BBB;
    min-width: 20px;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Combo Box */
QComboBox {
    background-color: #FFF;
    color: #333;
    border: 1px solid #CCC;
    padding: 5px;
}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
    top: 1px;
    left: 1px;
}

QComboBox::drop-down {
    width: 20px;
    border: none;
}

QComboBox:editable {
    background-color: #FFF;
}

QComboBox QAbstractItemView {
    color: #333;
    background-color: #FFF;
    selection-background-color: #DDD;
}

/* Spin Box */
QSpinBox {
    background-color: #FFF;
    color: #333;
    border: 1px solid #CCC;
    padding: 5px;
}

/* Slider */
QSlider::groove:horizontal {
    background-color: #CCC;
    height: 5px;
}

QSlider::handle:horizontal {
    background-color: #BBB;
    width: 15px;
    margin: -5px 0;
}

QSlider::groove:vertical {
    background-color: #CCC;
    width: 5px;
}

QSlider::handle:vertical {
    background-color: #BBB;
    height: 15px;
    margin: 0 -5px;
}

/* Radio Button */
QRadioButton {
    color: #333;
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
    color: #333;
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
    background-color: #CCC;
    color: #333;
    border: none;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #BBB;
}

/* Menu and Menu Bar */
QMenuBar {
    background-color: #DDD;
}

QMenuBar::item {
    color: #333;
}

QMenuBar::item:selected {
    background-color: #CCC;
}

QMenu {
    background-color: #DDD;
}

QMenu::item {
    color: #333;
}

QMenu::item:selected {
    background-color: #CCC;
}

/* Tool Tip */
QToolTip {
    background-color: #DDD;
    color: #333;
    border: none;
}

/* Tool Button */
QToolButton {
    background-color: #DDD;
    color: #333;
    border: 1px solid #CCC;
    padding: 3px;
    border-radius: 8px;
}

QToolButton:hover {
    background-color: #CCC;
}

QToolButton:pressed {
    background-color: #BBB;
}

/* Table Widget */
QTableWidget {
    border-style: solid;
    border-width: 1px;
    border-color: #CCC;
    border-radius: 0px;
    background-color: #FFF;
    color: #333;
    gridline-color: #CCC;
    outline: none;
}

QTableWidget QHeaderView::section {
    background-color: #DDD;
    color: #333;
    padding: 5px;
    border: 1px solid #CCC;
    font: 12pt "Microsoft YaHei";
}

QTableWidget QTableCornerButton::section {
    background-color: #DDD;
    color: #333;
}

QTableWidget::item {
    background-color: #FFF;
    color: #333;
}

QTableWidget::item:selected {
    background-color: #CCC;
}
"""
