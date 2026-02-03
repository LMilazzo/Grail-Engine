from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget


# >>> CONVERSATION AREA >>>
class Conversation(StyledWidget):
    def __init__(self, parent=None):
        super().__init__("Conversation")

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("ChatScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Internal container
        self.messages = StyledWidget("Messages")
        self.mlayout = QVBoxLayout(self.messages)

        # Message Spacing
        self.mlayout.setSpacing(15)
        self.mlayout.setContentsMargins(8, 8, 8, 8)
        self.mlayout.addStretch()

        # Set as content widget
        self.scroll_area.setWidget(self.messages)

        #Message Horz spacing
        self.HORIZONTAL_MARGIN = 15

        #Container Layout -V-
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)

        # Styling
        self.setStyleSheet("""
            QWidget#Conversation {
                background-color: #000000;
                border: 1px solid white;
                border-radius: 10%;
            }
            QWidget#ChatScrollArea{
                background-color: #000000;
                border: 0px;
            }
            QWidget#Messages{
                border: 0px;
                background-color: transparent;
            }
        """)
# <<< CONVERSATION AREA <<<
