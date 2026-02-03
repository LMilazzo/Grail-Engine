from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> CLEAR LAST CHAT BUTTON >>>
class ClearLastChatButton(QPushButton):
     def __init__(self, text="Clear Message"):
        super().__init__(text)

        # Set Name
        self.setObjectName("ClearLastMessageButton")

        # Styling
        self.setStyleSheet("""
            QPushButton#ClearLastMessageButton {
                border: 1px solid white;
                border-radius: 10%;
                background-color: #000000;
                color: white;
            }
        """)

        self.setFixedWidth(90)
        self.setFixedHeight(30)
# <<< CLEAR LAST CHAT BUTTON <<<
