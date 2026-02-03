from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.StyledWidget import StyledWidget

# >>> SYSTEM PROMPT INPUT >>>
class SystemPromptInput(StyledWidget):
    def __init__(self):
        super().__init__("SystemPromptInput")

        # Layout -V-
        layout = QVBoxLayout(self)

        # Styling
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

        # Text Area
        self.input = QTextEdit()

        # Set Name
        self.input.setObjectName("SystemPromptTextEdit")

        # Scroll bar policy
        self.input.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Size
        self.input.setFixedHeight(175)
        self.input.setFixedWidth(175)
        # IMPORTANT: prevent vertical expansion
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed
        )
        
        layout.addWidget(self.input)
# <<< SYSTEM PROMPT INPUT <<<
