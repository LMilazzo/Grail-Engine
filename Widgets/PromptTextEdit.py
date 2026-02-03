from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# >>> PROMPT TEXT EDIT SIGNALS >>>
class PromptTextEditSignals(QObject):
    sendRequested = pyqtSignal()
# <<< PROMPT TEXT EDIT SIGNALS <<<

# >>> PROMPT TEXT EDIT >>>
class PromptTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.signals = PromptTextEditSignals()

    def keyPressEvent(self, event):
        # Enter → send
        if event.key() == Qt.Key.Key_Return and not event.modifiers():
            self.signals.sendRequested.emit()
            event.accept()
        # Shift+Enter → newline
        else:
            super().keyPressEvent(event)
# <<< PROMPT TEXT EDIT <<<