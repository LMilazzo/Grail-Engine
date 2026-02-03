from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> SEND PROMPT BUTTON >>>
class SendPromptButton(QPushButton):
    def __init__(self, text="-->"):
        super().__init__(text)

        # Set Name
        self.setObjectName("SendPromptButton")

        # Styling
        self.setStyleSheet("""
            QPushButton#SendPromptButton {
                border: 1px solid white;
                border-radius: 10%;
                background-color: #000000;
                color: white;
            }
        """)

        # Size
        self.setFixedWidth(50)
        self.setFixedHeight(30)
# <<< SEND PROMPT BUTTON <<<