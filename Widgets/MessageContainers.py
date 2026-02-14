from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget
from Widgets.ChatBubble import UserBubble, BotBubble

from Utils.OllamaUtils import TokenCountEstimate_Prompt, TokenCountEstimate_String

# >>> PROMPT CONTAINER >>>
class UserContainer(StyledWidget):
    def __init__(self, info: dict, message_id: int):
        super().__init__("bubble"+str(message_id))

        # INFO
        self.info = info


        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------
        layout = QVBoxLayout(self)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet(f"""
            QWidget#{"info"} {{
                text-align: right;
                color: #545454;
                font-size: 10px;
                text-decoration: underline;
            }}
        """)

        #Spacing
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.setContentsMargins(0,0,0,0)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~


        #--------------------------------------------------  
        #------------------ INFO HEADER ------------------- 
        #--------------------------------------------------
        self.info_row = QHBoxLayout()

        self.header_format = "| Tokens: ~{} | T: {} | P: {} | Max T: {} |"

        # Create info label:
        # Refrence: #{
        #    "system": "",
        #    "temp": 0.9,
        #    "topP": 0.9,
        #    "topK": 40.0,
        #    "rep": 1.1,
        #    "tokens": 512,
        #    "tools": [],
        #    "model": "KURISU-1.5:latest",
        #   "prompt": "erfnjdfnkj",
        #    "id": 0,
        #    "token_estimate": 2
        #}
        self.info_lab = QLabel(self.header_format.format(
            self.info["token_estimate"], self.info["temp"], self.info["topP"], self.info["tokens"])
        )

        self.info_lab.setObjectName("info")
        
        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.info_lab.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        self.info_row.addWidget(self.info_lab)

        layout.addLayout(self.info_row)

        #--------------------------------------------------  
        #--------------- MESSAGE BUBBLE ------------------- 
        #--------------------------------------------------

        #Bubble Row
        self.bubble_row = QHBoxLayout()

        #Create Bubble
        self.bubble = UserBubble()

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.bubble.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        
        self.bubble_row.addStretch()

        self.bubble_row.addWidget(self.bubble)

        layout.addLayout(self.bubble_row)


        layout.addStretch()
    
#__________________________________________________________________________________________________________

    # Resets the text in the bubble
    def setText(self, text):
        self.bubble.set_text(text)

    # Returns the bubble plain text
    def toPlainText(self):
        return self.bubble.toPlainText()
    
    # Takes in a prompt dict and updates the into
    def updateTokens(self, tokens: int):
        self.info_lab.setText(self.header_format.format(
            tokens, self.info["temp"], self.info["topP"], self.info["tokens"])
        )

# <<< PROMPT CONTAINER <<<


# >>> PROMPT CONTAINER >>>
class BotContainer(StyledWidget):
    def __init__(self, info: dict, message_id: int):
        super().__init__("bubble"+str(message_id))

        # INFO
        self.info = info

        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------
        layout = QVBoxLayout(self)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet(f"""
            QWidget#{"info"} {{
                text-align: right;
                color: #545454;
                font-size: 10px;
                text-decoration: underline;
            }}
        """)

        #Spacing
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(6)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.setContentsMargins(0,0,0,0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~


        #--------------------------------------------------  
        #------------------ INFO HEADER ------------------- 
        #--------------------------------------------------
        self.info_row = QHBoxLayout()

        self.header_format = "| Tokens: ~{} | Model: {}"

        # Create info label:
        # Refrence: #{
        #    "system": "",
        #    "temp": 0.9,
        #    "topP": 0.9,
        #    "topK": 40.0,
        #    "rep": 1.1,
        #    "tokens": 512,
        #    "tools": [],
        #    "model": "KURISU-1.5:latest",
        #   "prompt": "erfnjdfnkj",
        #    "id": 0,
        #    "token_estimate": 2
        #}
        self.info_lab = QLabel(self.header_format.format("To Do", self.info["model"]))

        self.info_lab.setObjectName("info")

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.info_lab.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.info_row.addWidget(self.info_lab)

        layout.addLayout(self.info_row)

        #--------------------------------------------------  
        #--------------- MESSAGE BUBBLE ------------------- 
        #--------------------------------------------------
        self.bubble_row = QHBoxLayout()

        self.bubble = BotBubble()
        
        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.bubble.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        self.bubble_row.addWidget(self.bubble)
        self.bubble_row.addStretch()

        layout.addLayout(self.bubble_row)

        layout.addStretch()
    
    # Resets the text in the bubble
    def setText(self, text):
        self.bubble.set_text(text)
        self.update_tokens()

    # Returns the bubble plain text
    def toPlainText(self):
        return self.bubble.toPlainText()
    
    # Takes in a prompt dict and updates the into
    def update_tokens(self):
        tokens = TokenCountEstimate_String(self.toPlainText())
        self.info_lab.setText(self.header_format.format(tokens, self.info["model"]))
# <<< PROMPT CONTAINER <<<