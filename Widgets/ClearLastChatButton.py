from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> CLEAR LAST CHAT BUTTON >>>
class ClearLastChatButton(QPushButton):
     def __init__(self, text="Clear Message"):
        super().__init__(text)

        # Set Name
        self.setObjectName("ClearLastMessageButton")

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QPushButton#ClearLastMessageButton {
                border: 1px solid white;
                border-radius: 10%;
                background-color: #000000;
                color: white;
            }
            QPushButton#ClearLastMessageButton:hover {
                background-color: #633636; 
            }    
        """)

        self.setFixedWidth(90)
        self.setFixedHeight(30)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

# <<< CLEAR LAST CHAT BUTTON <<<
