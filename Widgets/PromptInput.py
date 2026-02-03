from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Widgets.PromptTextEdit import PromptTextEdit
from Widgets.StyledWidget import StyledWidget

# >>> PROMPT TEXT EDIT SIGNALS >>>
class PromptInputSignals(QObject):
    sendRequested = pyqtSignal()
# <<< PROMPT TEXT EDIT SIGNALS <<<

# >>> PROMPT INPUT >>>
class PromptInput(StyledWidget):
    def __init__(self):
        super().__init__("PromptInput")
        
        self.signals = PromptInputSignals()

        # Layout -H-
        layout = QHBoxLayout(self)
        
        # Styling
        self.setStyleSheet("""
            QWidget#PromptInput {
                background-color: #000000;
            }
            QWidget#PromptInputBox{
                background-color: #000000;
                border: 1px solid white;
                border-radius: 10%;
                color: white;
                padding: 2px;
            }
        """)
        
        # Max Height
        self.setFixedHeight(100)

        # Input box 
        self.input_box = PromptTextEdit()

        # Set Name
        self.input_box.setObjectName("PromptInputBox")

        # Default
        self.input_box.setPlaceholderText("<!...>")

        # Starting Size
        self.input_box.setFixedHeight(40)

        # Connect resizing and sending functions
        self.input_box.textChanged.connect(self._resize)
        self.input_box.signals.sendRequested.connect(self.signals.sendRequested)

        layout.addWidget(self.input_box)

    # Resizes the Text box to fit the full text ( Only Height wise )
    def _resize(self):
        padding = 8

        # Calculate document height
        doc_height = self.input_box.document().size().height()
        new_height = int(doc_height + padding)

        # Limits
        min_height = 40
        max_height = self.height() - 10  # stay within container size

        # Clamp height
        final_height = max(min_height, min(new_height, max_height))

        self.input_box.setFixedHeight(final_height)

        # Enable scrolling only when max reached
        if new_height > max_height:
            self.input_box.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        else:
            self.input_box.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    # Returns the prompt entry as plain text
    def getText(self):
        return self.input_box.toPlainText().strip()

    # Clears the prompt entry field
    def clear(self):
        self.input_box.clear()
        self.input_box.setFixedHeight(40)
# <<< PROMPT INPUT <<<