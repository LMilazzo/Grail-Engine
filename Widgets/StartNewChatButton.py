from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> START NEW CHAT BUTTON >>>
class StartNewChatButton(QPushButton):
    def __init__(self, text="New Chat"):
        super().__init__(text)

        # Set Name
        self.setObjectName("StartNewChatButton")

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QPushButton#StartNewChatButton {
                border: 1px solid white;
                border-radius: 10%;
                background-color: #000000;
                color: white;
            }
            QPushButton#StartNewChatButton:hover {
                background-color: green; 
            }    
        """)

        self.setFixedWidth(65)
        self.setFixedHeight(30)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

# <<< START NEW CHAT BUTTON <<<

