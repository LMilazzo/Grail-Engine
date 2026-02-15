from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout

from GUI.ChatArea import ChatArea

from Widgets.MessageContainers import UserContainer, BotContainer

from Utils.OllamaUtils import TokenCountEstimate_String, TokenCountEstimate_Prompt
from Utils.PyQt_Utils import clear_layout

#**************  SIGNALS *****************
class ControllerSignals(QObject):
    pass

#**************  SIGNALS *****************

# >>> CHAT CONTROLLER >>>
class ChatController():
    def __init__(self, ChatArea: ChatArea):

        #**************  SIGNALS *****************
        self.signals = ControllerSignals()

        #--------------------------------------------------  
        #------------------- UI OBJECTS -------------------
        #--------------------------------------------------
        self.ChatArea = ChatArea

        #--------------------------------------------------
        #                    MESSAGE ID
        self._NEXT_ID = 0

        #--------------------------------------------------
        #                    LAST MESSAGES
        self.last_prompt = None
        self.last_response = None
        self.active_streaming = False

#__________________________________________________________________________________________________________

    def addPrompt(self, params):

        #{
        #    "system": "",
        #    "temp": 0.9,
        #    "topP": 0.9,
        #    "topK": 40.0,
        #    "rep": 1.1,
        #    "tokens": 512,
        #    "tools": [],
        #    "model": "KURISU-1.5:latest",
        #   "prompt": "erfnjdfnkj",
        #    "id": 0,
        #    "token_estimate": 2
        #}

        params["id"] = self._NEXT_ID
        params["token_estimate"] = TokenCountEstimate_String(params["prompt"])

        self._nextID()

        # +++++ CREATE MESSAGE BUBBLE +++++
        user_message = UserContainer(info=params, message_id=params["id"])
        user_message.setText(params["prompt"])

        self.last_prompt = user_message

        # Add Message to the ChatArea Widget UI
        self.ChatArea.addUserMessage(user_message)

        #Scroll to bottom
        bar = self.ChatArea.conversation.scroll_area.verticalScrollBar()
        bar.setValue(bar.maximum())

    def _init_Response(self, params):

        # +++++ CREATE MESSAGE BUBBLE +++++
        assistant_message = BotContainer(info=params, message_id=self._NEXT_ID)
        assistant_message.setText("")

        self._nextID()

        self.last_response = assistant_message

        self.ChatArea.addAssistantMessage(assistant_message)

    def _stop_Response(self):
        self.active_streaming = False
#__________________________________________________________________________________________________________
    
    def updateLatestPrompt(self, prompt):
        tokens = TokenCountEstimate_Prompt(prompt)

        self.last_prompt.updateTokens(tokens)

    def stream_to_latest_assistant(self, chunk):

        self.last_response.setText(self.last_response.toPlainText() + chunk)

        #Scroll to bottom
        bar = self.ChatArea.conversation.scroll_area.verticalScrollBar()
        bar.setValue(bar.maximum())

#__________________________________________________________________________________________________________

    def clear(self):

        for i in reversed(range(self.ChatArea.conversation.MESSAGE_layout.count())): 

            if isinstance(self.ChatArea.conversation.MESSAGE_layout.itemAt(i), QHBoxLayout):
                
                #Clears the sublayout of the message
                clear_layout(self, self.ChatArea.conversation.MESSAGE_layout.itemAt(i))
                
                #Finally remove for good
                self.ChatArea.conversation.MESSAGE_layout.takeAt(i)

    def undo(self):
        
        count = self.ChatArea.conversation.MESSAGE_layout.count()

        # When the latest prompt response pair is complete count will always be odd.
        if not count > 1:
            return

        for i in range(0, 2):

            if isinstance(self.ChatArea.conversation.MESSAGE_layout.itemAt(count-2), QHBoxLayout):
                
                #Clears the sublayout of the message
                clear_layout(self, self.ChatArea.conversation.MESSAGE_layout.itemAt(count-2))
                
                #Finally remove for good
                self.ChatArea.conversation.MESSAGE_layout.takeAt(count-2)

                count -= 1

#__________________________________________________________________________________________________________

    def _nextID(self):
        self._NEXT_ID += 1




# <<< CHAT CONTROLLER <<<