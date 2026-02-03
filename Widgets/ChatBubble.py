from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> CHAT BUBBLE >>>
class ChatBubble(QTextEdit):
    def __init__(self, background="#000000", text="white", border="#white", parent=None):
        super().__init__(parent)

        # Sizing
        self.maxWidth = 350
        self.padding = 6
        self.borderW = 2
        self.extraSpace = self.padding * 2 + self.borderW * 2

        # Text edit settings
        self.setReadOnly(True)
        self.setFont(QFont("Inter", 11))

        # Style
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {background};
                border: {self.borderW}px solid {border};
                border-radius: 8px;
                padding: {self.padding}px;
                color: {text};
            }}
        """)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def set_text(self, text: str):
        super().setPlainText(text)
        self._resize()

    def _resize(self):

        font = self.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        #print(fontMetrics.size(0, self.toPlainText()))
        textSize = fontMetrics.size(0, self.toPlainText())
        
        w = min(textSize.width() + self.extraSpace, self.maxWidth)
        self.setFixedWidth(w + self.extraSpace + 10)
        self.document().setTextWidth(w)

        #print(self.document().size())
        self.setFixedHeight(int(self.document().size().height()) + self.extraSpace)
# <<< CHAT BUBBLE <<<


# >>> USER MESSAGE >>>
class UserBubble(ChatBubble):
    def __init__(self, parent=None):
        super().__init__(background="#000000", text="#b3b3b3", border="#633636", parent=parent)
        self.maxWidth = 350
# <<< USER MESSAGE <<<


# >>> BOT MESSAGE >>>
class BotBubble(ChatBubble):
    def __init__(self, parent=None):
        super().__init__(background="#000000", text="#d3b6d8", border="#361f3d", parent=parent)
        self.maxWidth = 500

    def _resize(self):

        font = self.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        #print(fontMetrics.size(0, self.toPlainText()))
        textSize = fontMetrics.size(0, self.toPlainText())
        
        w = min(textSize.width() + self.extraSpace, self.maxWidth)
        self.setFixedWidth(w + self.extraSpace + 15)
        self.document().setTextWidth(w)

        #print(self.document().size())
        self.setFixedHeight(int(self.document().size().height()) + self.extraSpace + 5)
# <<< BOT MESSAGE <<<