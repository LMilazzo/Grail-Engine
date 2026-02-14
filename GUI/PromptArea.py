from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import QObject, pyqtSignal

from Widgets.ModelSelection import ModelSelection
from Widgets.PromptInput import PromptInput
from Widgets.SendPromptButton import SendPromptButton

#**************  SIGNALS *****************
class WidgetSignals(QObject):

    # Signal activates when a prompt is sent releasing 
    # the selected model and the prompt 
    prompt_requested = pyqtSignal(str, str) #(MODEL, PROMPT)

#**************  SIGNALS *****************

# >>> PROMPT AREA >>>
class PromptArea(QWidget):
    def __init__(self):
        super().__init__()

        #**************  SIGNALS *****************
        self.signals = WidgetSignals()

        #--------------------------------------------------  
        #------------------ CORE LAYOUT ------------------- 
        #--------------------------------------------------

        #|-------------------------------------------------|
        #|                   ____________________          |
        #| MODEL SELECTION  | INPUT AREA        |   |->|   |
        #|                  --------------------           |
        #|-------------------------------------------------|

        layout = QHBoxLayout(self)

        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~
        self.setStyleSheet("""
            QWidget#PromptArea {
                border: 1px solid white;
                background-color: #000000;
                border-radius: 10%;
            }
        """)
        
        # Max Height
        self.setFixedHeight(110)
        #~~ ~~ ~~ ~~ ~~ ~~~ MAIN STYLE ~~ ~~ ~~ ~~ ~~ ~~ ~~

        
        #--------------------------------------------------  
        #----------- MODEL SELECTION WIDGET --------------- 
        #--------------------------------------------------
        self.model_selection = ModelSelection()
        layout.addWidget(self.model_selection)

        #--------------------------------------------------  
        #------------- PROMPT INPUT WIDGET ---------------- 
        #--------------------------------------------------
        self.prompt_input = PromptInput()
        layout.addWidget(self.prompt_input)

        self.prompt_input.signals.send_prompt.connect(self._send_prompt_emit)

        #--------------------------------------------------  
        #-------------- SEND PROMPT WIDGET ---------------- 
        #--------------------------------------------------
        self.send_prompt_btn = SendPromptButton()
        layout.addWidget(self.send_prompt_btn)

        self.send_prompt_btn.clicked.connect(self._send_prompt_emit)

#__________________________________________________________________________________________________________

    # Emits a signal with the prompt and selected  model
    def _send_prompt_emit(self):

        #Get Data
        model = self.model_selection.select_box.currentText()
        prompt = self.prompt_input.getText()

        # Reset box
        self.prompt_input.clear()

        self.signals.prompt_requested.emit(model, prompt)
        
    # Sets the models in the model selection drop down
    def setModels(self, model_list: list):
        self.model_selection.addModels(model_list)

# <<< PROMPT AREA <<<