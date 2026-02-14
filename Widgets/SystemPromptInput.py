from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget

# >>> SYSTEM PROMPT INPUT >>>
class SystemPromptInput(StyledWidget):
    def __init__(self):
        super().__init__("SystemPromptInput")

        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------

        layout = QVBoxLayout(self)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QWidget#SystemPromptInput {
                background-color: #000000;
                color: #FFB2B2;
            }
            QWidget#SystemPromptTextEdit {
                background-color: #000000; 
                color: white; 
                border: 1px solid white;
                border-radius: 10%;
            }
        """)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

        #--------------------------------------------------  
        #---------------- INPUT WIDGET -------------------- 
        #--------------------------------------------------  
        self.input = QTextEdit()

        # Set Name
        self.input.setObjectName("SystemPromptTextEdit")

        #~~ ~~ ~~ ~~ ~~ ~~ ~~ STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.input.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.input.setFixedHeight(175)

        layout.addWidget(self.input)

#__________________________________________________________________________________________________________

    def getText(self):
        return self.input.toPlainText()

# <<< SYSTEM PROMPT INPUT <<<
