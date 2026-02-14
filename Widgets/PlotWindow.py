from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView


# >>> PLOT WINDOW >>>
class PlotWindow(QWebEngineView):
    def __init__(self, width: int):
        super().__init__()

        self.setObjectName("plotwindow")

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QWebEngineView#plotwindow {
                background-color: #000000;
                border: 1px solid red;
            }
        """)
        
        self.setFixedWidth(width)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~


# <<< PLOT WINDOW <<<