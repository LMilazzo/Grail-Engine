from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

#**************  SIGNALS *****************
class PromptTextEditSignals(QObject):

    #Emits a signal when the enter key is pressed sending the prompt
    enter_pressed = pyqtSignal()

#**************  SIGNALS *****************

# >>> PROMPT TEXT EDIT >>>
class PromptTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

        #**************  SIGNALS *****************
        self.signals = PromptTextEditSignals()

#__________________________________________________________________________________________________________

    #Connects the 'Enter' or 'Return' Key to the 'enter_pressed' signal
    def keyPressEvent(self, event):
        
        # Enter → send
        if event.key() == Qt.Key.Key_Return and not event.modifiers():

            self.signals.enter_pressed.emit()

            event.accept()

        else:
            super().keyPressEvent(event)

# <<< PROMPT TEXT EDIT <<<