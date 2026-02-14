from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

USER_MAX_WIDTH = 350
ASSISTANT_MAX_WIDTH = 500

# >>> CHAT BUBBLE >>>
class ChatBubble(QTextEdit):
    def __init__(self, background="#000000", text="white", border="#white", parent=None):
        super().__init__(parent)

        self.maxWidth = 350
        self.padding = 6
        self.borderW = 2
        self.extraSpace = self.padding * 2 + self.borderW * 2

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {background};
                border: {self.borderW}px solid {border};
                border-radius: 8px;
                padding: {self.padding}px;
                color: {text};
            }}
        """)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

        self.setReadOnly(True)
        self.setFont(QFont("Verdana", 11))

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

#__________________________________________________________________________________________________________

    def set_text(self, text: str):
        super().setPlainText(text)
        self._resize()

#__________________________________________________________________________________________________________

    def _resize(self):

        font = self.document().defaultFont()
        fontMetrics = QFontMetrics(font)

        textSize = fontMetrics.size(0, self.toPlainText())
        
        w = min(textSize.width() + self.extraSpace, self.maxWidth)

        self.setFixedWidth(w + self.extraSpace + 10)
        
        self.document().setTextWidth(w)

        self.setFixedHeight(int(self.document().size().height()) + self.extraSpace)

# <<< CHAT BUBBLE <<<


# >>> USER MESSAGE >>>
class UserBubble(ChatBubble):
    def __init__(self, parent=None):
        super().__init__(background="#000000", text="#BC8888", border="#633636", parent=parent)
        
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.maxWidth = USER_MAX_WIDTH
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
# <<< USER MESSAGE <<<


# >>> BOT MESSAGE >>>
class BotBubble(ChatBubble):
    def __init__(self, parent=None):
        super().__init__(background="#000000", text="#d3b6d8", border="#361f3d", parent=parent)
        
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.maxWidth = ASSISTANT_MAX_WIDTH
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

#__________________________________________________________________________________________________________

    def _resize(self):

        font = self.document().defaultFont()

        fontMetrics = QFontMetrics(font)

        textSize = fontMetrics.size(0, self.toPlainText())
        
        w = min(textSize.width() + self.extraSpace, self.maxWidth)
        
        self.setFixedWidth(w + self.extraSpace + 15)
        
        self.document().setTextWidth(w)

        self.setFixedHeight(int(self.document().size().height()) + self.extraSpace + 5)
# <<< BOT MESSAGE <<<