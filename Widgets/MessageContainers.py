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

        #Info about prompt
        self.info = info

        # Layout
        layout = QVBoxLayout(self)

        #Spacing
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(6)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.setContentsMargins(0,0,0,0)

        # Styling
        self.setStyleSheet(f"""
            QWidget#{"info"} {{
                text-align: right;
                color: #545454;
                font-size: 10px;
                text-decoration: underline;
            }}
        """)

        #Info Row
        self.info_row = QHBoxLayout()

        #Bubble Row
        self.bubble_row = QHBoxLayout()

        # Create Bubble
        self.bubble = UserBubble()
        self.bubble.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.bubble_row.addStretch()

        self.bubble_row.addWidget(self.bubble)

        # Update Token 
        self.tokens = TokenCountEstimate_Prompt(info)


        # Create info label:
        # Refrence: {"model" : f"{self.model}", "messages" : messages,"options": {
            # "temperature": self.temp, "top_p": self.topP, "top_k": self.topK, "repeat_penalty": self.repeat, "num_predict": self.max_tokens} 
        self.info_lab = QLabel(f"| Tokens: ~{self.tokens} | T: {self.info['options']['temperature']} | P: {self.info['options']['top_p']} | Max T: {self.info['options']['num_predict']} |")
        self.info_lab.setObjectName("info")
        self.info_lab.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        self.info_row.addWidget(self.info_lab)

        layout.addLayout(self.info_row)
        layout.addLayout(self.bubble_row)

        layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        layout.addStretch()
    
    # Resets the text in the bubble
    def setText(self, text):
        self.bubble.set_text(text)

    # Returns the bubble plain text
    def toPlainText(self):
        return self.bubble.toPlainText()
    
    # Takes in a prompt dict and updates the into
    def update_tokens(self, prompt: dict):
        self.tokens = TokenCountEstimate_Prompt(prompt)
        self.info_lab.setText(f"| Tokens: ~{self.tokens} | T: {self.info['options']['temperature']} | P: {self.info['options']['top_p']} | Max T: {self.info['options']['num_predict']} |")
# <<< PROMPT CONTAINER <<<


# >>> PROMPT CONTAINER >>>
class BotContainer(StyledWidget):
    def __init__(self, info: dict, message_id: int):
        super().__init__("bubble"+str(message_id))

        #Info about prompt
        self.info = info

        # Layout
        layout = QVBoxLayout(self)

        #Spacing
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(6)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.setContentsMargins(0,0,0,0)

        # Styling
        self.setStyleSheet(f"""
            QWidget#{"info"} {{
                text-align: right;
                color: #545454;
                font-size: 10px;
                text-decoration: underline;
            }}
        """)

        #Info Row
        self.info_row = QHBoxLayout()

        #Bubble Row
        self.bubble_row = QHBoxLayout()

        # Create Bubble
        self.bubble = BotBubble()
        self.bubble.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        self.bubble_row.addWidget(self.bubble)
        self.bubble_row.addStretch()

        # Update Token 
        self.tokens = TokenCountEstimate_Prompt(info)


        # Create info label:
        # Refrence: {"model" : f"{self.model}", "messages" : messages,"options": {
            # "temperature": self.temp, "top_p": self.topP, "top_k": self.topK, "repeat_penalty": self.repeat, "num_predict": self.max_tokens} 
        self.info_lab = QLabel(f"| Tokens: ~{self.tokens} | Model: {self.info['model']}")
        self.info_lab.setObjectName("info")
        self.info_lab.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.info_row.addWidget(self.info_lab)

        layout.addLayout(self.info_row)
        layout.addLayout(self.bubble_row)

        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
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
        self.tokens = TokenCountEstimate_String(self.toPlainText())
        self.info_lab.setText(f"| Tokens: ~{self.tokens} | {self.info['model']} |")
# <<< PROMPT CONTAINER <<<