# -*- coding: utf-8 -*-
Trans = """
QWidget {
    
    color: #EEE;
    font-size: 16px;
    border-radius: 5px;
}

/* Label */
QLabel {
    color: #EEE;
    font-size: 18px;
    font-family: 'Arial';
}

QTextEdit{
    background-color: transparent;
    color: rgb(244, 244, 244);
    border:1px solid black;
    border-color: #edd1d8;
    font: regular 12pt 华为仿宋;
}

QToolButton{
background-color: transparent;
}

QToolButton::hover{
     border:0px;
}

QComboBox {
    background-color: transparent;
    border: 1px solid #bcbcbc;
    border-radius: 5px;
    padding: 5px;
    min-width: 100px;
    color: darkgray;
    font: italic 12pt "Consolas";
}

QComboBox::drop-down {
    width: 0px;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid darkgray;
    color: #333333;
}

QComboBox QAbstractItemView::item {
    background-color: white;
    color: #333333;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #007BFF;
    color: white;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #007BFF;
    color: white;
}

QComboBox QListView {
    background-color: white;
}

QComboBox QAbstractScrollArea {
    background-color: white;
}

QMenuBar{
    border-color: transparent;
}

QScrollBar:vertical {
    background: transparent;
    padding:2px;
    border-radius:4px;
    width:8px;
}

QScrollBar::handle:vertical{
    background:#9acd32;
    min-height:8px;
    border-radius:4px;
}

QScrollBar::handle:vertical:hover{
   background:#9eb764;
}

QScrollBar::handle:vertical:pressed{
   background:#9eb764;
}

QScrollBar::add-page:vertical{
    background:none;
}

QScrollBar::sub-page:vertical{
   background:none;
}

QScrollBar::add-line:vertical{
   background:none;
}

QScrollBar::sub-line:vertical{
   background:none;
}

QScrollArea{
    border:0px;
}

QScrollBar:horizontal{
   background:transparent;
   padding:0px;
   border-radius:4px;
   max-height:6px;
}

QScrollBar::handle:horizontal{
    background:#9acd32;
    min-width:8px;
    border-radius:4px;
}

QScrollBar::handle:horizontal:hover{
    background:#9eb764;
}

QScrollBar::handle:horizontal:pressed{
    background:#9eb764;
}

QScrollBar::add-page:horizontal{
    background:none;
}

QScrollBar::sub-page:horizontal{
    background:none;
}

QScrollBar::add-line:horizontal{
    background:none;
}
QScrollBar::sub-line:horizontal{
    background:none;
}

QTableWidget{
    color:#f3f9f1;
    background:transparent;
    border:1px solid #00e09e;
    alternate-background-color:transparent;
    gridline-color:#00e09e;
}

QTableWidget::item:selected{
    color:rgba(240,240,244,60%);
    background:rgba(243,249,241,40%);
}

QTableWidget::item:hover{
    background:rgba(240,240,244,40%);
}

QHeaderView{
    background:transparent;
}

QHeaderView::section{
    background:rgba(240,240,244,10%);
    margin:0px;
    color:rgba(243,249,241,100%);
    border:1px solid #00e09e;
    border-left-width:0;
}

QScrollBar:vertical{
    background:#CCCCCC;
    padding:0px;
    border-radius:2px;
    max-width:6px;
}

QScrollBar::handle:vertical{
    background:rgba(255,179,167,80%);
}

QScrollBar::handle:hover:vertical,
    QScrollBar::handle:pressed:vertical{
    background:#A7A7A7;
}

QScrollBar::sub-page:vertical{
    background:transparent;
}

QScrollBar::add-page:vertical{
    background:transparent;
}

QScrollBar::add-line:vertical{
    background:none;
}

QScrollBar::sub-line:vertical{
    background:none;
}

QMessageBox {
    background-color: #ffffff;
    border-radius: 10px;
}

QMessageBox QLabel {
    color: #000000;
    font-size: 18px;
    font-family: 'Arial';
}

QMessageBox QPushButton {
    background-color: transparent;
    border-width: 1px;
    border-style: solid;
    border-color: gray;
    color: #000000;
    padding: 10px 20px;
    text-align: center;
    display: inline-block;
    font-size: 16px;
    margin: 20px 20px;
    cursor: pointer;
    border-radius: 10px;
}

QMessageBox QPushButton:hover {
    border: 1px solid qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #800080, stop: 1 #0000ff);
}

QMessageBox QPushButton:pressed {
    border: 1px solid #00bfff;
    background: rgba(0, 0, 0, 0.1);
    box-shadow: inset 0 0 5px #1e90ff;
}


"""
