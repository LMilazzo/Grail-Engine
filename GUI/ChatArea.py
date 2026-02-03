from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from Controllers.ChatController import ChatController

from Utils.OllamaUtils import *

from Widgets.Conversation import Conversation
from Widgets.ModelSelection import ModelSelection
from Widgets.PromptInput import PromptInput
from Widgets.SendPromptButton import SendPromptButton

# >>> CHAT AREA >>>
class ChatArea(QWidget):
    def __init__(self):
        super().__init__()

        #Layout -V-
        layout = QVBoxLayout(self)
        
        # Styling
        self.setStyleSheet("""
            QWidget#ChatArea {
                border: 1px solid white;
                background-color: #000000;
                border-radius: 10%;
            }
        """)

        #Add conversation area as top element
        self.conversation = Conversation()
        layout.addWidget(self.conversation)

        #Create sub layout beneath for horizontal elements
        input_layout = QHBoxLayout()
        
        #Add model selection
        self.model_selection = ModelSelection()
        input_layout.addWidget(self.model_selection)

        #Add Prompt Input
        self.prompt_input = PromptInput()
        self.prompt_input.signals.sendRequested.connect(self.send_prompt) #Connect "Enter" btn/key to send prompt
        input_layout.addWidget(self.prompt_input)

        #Add Prompt Send Button
        self.send_prompt_btn = SendPromptButton()
        self.send_prompt_btn.clicked.connect(self.send_prompt) #Connect send_prompt method
        input_layout.addWidget(self.send_prompt_btn)

        layout.addLayout(input_layout) # Add to parent layout

        # --- Methods ---

    # Submits the currently typed promt to the controller for processing
    def send_prompt(self):

        # UI not finished setting up
        if not self.chat_controller:
            return

        # There is an active prompt wait until its finished to prevent overhead
        if self.chat_controller.activePrompt():
            return
        
        prompt = self.prompt_input.getText()

        # return if the prompt is empty
        if not prompt: 
            return
        
        # Clear the prompt box
        self.prompt_input.input_box.clear()

        # USE CONTROLLER TO SEND THREAD AND GET RESPONSE
        self.chat_controller.handlePrompt(prompt)
    
    # Assigns a controller to this chat area 
    def setChatController(self, controller: ChatController):
        
        # Set Controller
        self.chat_controller = controller

        #Add models to Model Selection
        self.model_selection.add_models(self.chat_controller.getModels())
# <<< CHAT AREA <<<