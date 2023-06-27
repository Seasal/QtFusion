login_trans = """

QPushButton {
    border: none;
    border-radius: 6px;
    background-color: transparent;
}
QPushButton:hover {
    background-color: rgb(26, 122, 244);
}
QPushButton:pressed {
    background-color: transparent;
}

QToolButton{
    background-color: transparent;
    font: 10pt "微软雅黑";
    color: rgb(100, 100, 100);
    border:5px}

QToolButton::hover{
    border:0px;
    color: rgb(26, 122, 244);
}

QLineEdit{
    font: 12pt "微软雅黑";
    background-color: transparent;
    border:0px;
    color: rgb(107, 107, 107);
}

QLabel{
    background-color: transparent;
}

QCheckBox{
    font: 10pt "微软雅黑";
    color: rgb(100, 100, 100);
    spacing: 5px;
    background-color: transparent;
}

 QCheckBox::indicator {
     width: 18px;
     height: 18px;
 }

QCheckBox::indicator:unchecked {
     border-image: url(:/default_icons/check_unchecked.png);
 }

 QCheckBox::indicator:checked {
     border-image: url(:/default_icons/check_checked.png);
 }

 QTabWidget::pane{
    min-width:70px;
    min-height:25px;
    border-top: 0px solid;
    background-color: transparent;
 }

QTabBar::tab {
    font-size:10px;
    min-width:70px;
    min-height:25px;
    color: black;
    font:12px "Microsoft YaHei";
    border: -1px solid;
}

QTabBar::tab:selected{
    min-width:70px;
    min-height:25px;
    color: black;
    font:11px "Microsoft YaHei";
    border: 0px solid;
    border-bottom: 0px solid;
    border-color: #4796f0;
}

"""