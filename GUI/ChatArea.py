from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from Utils.OllamaUtils import *

from Widgets.Conversation import Conversation
from Widgets.ModelSelection import ModelSelection
from Widgets.PromptInput import PromptInput
from Widgets.SendPromptButton import SendPromptButton
from Widgets.MessageContainers import UserContainer, BotContainer

# >>> CHAT AREA >>>

BUBBLE_HORIZONTAL_MARGIN = 15

class ChatArea(QWidget):
    def __init__(self):
        super().__init__()

        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------
        #               Conversation WIDGET
        #|-------------------------------------------------|
        #|                                    ......       |
        #|                               ------------      |
        #|                              |            |     |
        #|                               -----------       |
        #|                                                 |
        #|      ......                                     |
        #|     ------------                                |
        #|    |            |                               |
        #|    |            |                               |
        #|    |            |                               |
        #|     -----------                                 |
        #|                                                 |
        #|-------------------------------------------------|

        layout = QVBoxLayout(self)
        
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QWidget#ChatArea {
                border: 1px solid white;
                background-color: #000000;
                border-radius: 10%;
            }
        """)
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setOffset(5, 5)
        self.shadow.setColor(QColor("#633636"))

        self.setGraphicsEffect(self.shadow)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~


        #--------------------------------------------------  
        #-------------- CONVERSATION WIDGET --------------- 
        #--------------------------------------------------

        self.conversation = Conversation()
        layout.addWidget(self.conversation)

#__________________________________________________________________________________________________________
    def addUserMessage(self, item: UserContainer):
        
        # Message Row
        row = QHBoxLayout()

        row.setContentsMargins(0, 0, BUBBLE_HORIZONTAL_MARGIN, 0)

        row.addStretch()

        row.addWidget(item)

        self.conversation.MESSAGE_layout.insertLayout(self.conversation.MESSAGE_layout.count() - 1, row)

    def addAssistantMessage(self, item: BotContainer):

        # Message Row
        row = QHBoxLayout()

        row.setContentsMargins(BUBBLE_HORIZONTAL_MARGIN, 0, 0, 0)

        row.addWidget(item)

        row.addStretch()

        self.conversation.MESSAGE_layout.insertLayout(self.conversation.MESSAGE_layout.count() - 1, row)

#__________________________________________________________________________________________________________

    def updateShadow(self, color: QColor):
        self.shadow.setColor(color)

# <<< CHAT AREA <<<