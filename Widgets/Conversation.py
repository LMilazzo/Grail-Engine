from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget


# >>> CONVERSATION AREA >>>
class Conversation(StyledWidget):
    def __init__(self, parent=None):
        super().__init__("Conversation")

        #--------------------------------------------------  
        #--------------- SCROLL CONTAINER ----------------- 
        #--------------------------------------------------
        layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("ChatScrollArea")

        #Container Layout -V-
        layout.addWidget(self.scroll_area)

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        #--------------------------------------------------  
        #-------------- MESSAGE CONTAINER ----------------- 
        #--------------------------------------------------
        self.messages = StyledWidget("Messages")
        self.MESSAGE_layout = QVBoxLayout(self.messages)

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.MESSAGE_layout.setSpacing(15)
        self.MESSAGE_layout.setContentsMargins(8, 8, 8, 8)
        self.MESSAGE_layout.addStretch()

        # CONNECT SCROLL AREA AND MESSAGE CONTAINER
        self.scroll_area.setWidget(self.messages)


        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
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
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

# <<< CONVERSATION AREA <<<
