from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> CLEAR HISTORY BUTTON >>>
class ClearHistoryButton(QPushButton):
    def __init__(self, text="Clear Chat"):
        super().__init__(text)

        # Set Name
        self.setObjectName("ClearHistoryButton")

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QPushButton#ClearHistoryButton {
                border: 1px solid white;
                border-radius: 10%;
                background-color: #000000;
                color: white;
            }
            QPushButton#ClearHistoryButton:hover {
                background-color: #633636; 
            }    
        """)

        self.setFixedWidth(65)
        self.setFixedHeight(30)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

# <<< CLEAR HISTORY BUTTON <<<

