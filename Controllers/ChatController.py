
from PyQt6.QtWidgets import *

from Controllers.OllamaWorker import *
from Controllers.MemoryManager import *
from Controllers.Prompt import *
from Controllers.ToolController import *

from ToolRegistry.Registry import OLLAMA_TOOLS, AVAILABLE_TOOLS

from Utils.OllamaUtils import *
from Utils.PyQt_Utils import *

from Widgets.MessageContainers import UserContainer, BotContainer

# >>> CHAT CONTROLLER >>>
class ChatController(QObject):
    
    # __init__ 
    def __init__(self, chat_area: "ChatArea", sidebar: "SideBar"):
        super().__init__()

        # Controllers
        self.memManager = MemoryManager(window=12) #Initialize memory manager with default 12
        self.toolController = ToolController()

        # Temp Storage
        self.last_response = [] # A list of chunks for the current working response

        # Models
        self.models = listModels()

        # Tool Registry info
        self.AVAILABLE_TOOLS = AVAILABLE_TOOLS
        self.active_tools = {}
        self.TOOL_REGISTRY = OLLAMA_TOOLS 
        # UI Refrences
        self._conversation = chat_area.conversation
        self._chat_area = chat_area
        self._sidebar = sidebar

        # Next_id
        self.next_id = 0

        # Determines if there is an actively running prompt to prevent overlap
        self.ACTIVE_PROMPT = False

    # Builds the current user prompt into a proper prompt object with the correct structure
    def build_prompt(self, user: str):

        p = Prompt(
            model = self._chat_area.model_selection.model_selection.currentText(),
            text = user, #Current user prompt
            system = self._sidebar.system_prompt_input.input.toPlainText(), #System prompt
            temp = self._sidebar.temp_control.value(),
            topK = self._sidebar.topK_control.value(),
            repeat = self._sidebar.repeat_control.value(),
            topP = self._sidebar.topP_control.value(),
            max_tokens = self._sidebar.token_control.value()
        )

        #LONG TERM MEMORY SEARCH USING A DB CONTROLLER RETURNS ITEMS
        #DO SOMETHING LIKE
        #p.editLongTermHistory

        # Add Conversation history to the prompt
        p.editConvHistory(self.memManager.getRecent())

        # Add the currently selected tools
        p.setTools(self.getActiveTools())

        #Build and return the prompt object
        return p.build()

    # Receives a prompt from the chat area and processes the prompt
    # A Prompt object is made a built with the proper structure before being 
    # passed to the worker node to make an api call.
    def handlePrompt(self, prompt: str):

        self.ACTIVE_PROMPT = True

        # Build a prompt with proper memory and prompt structure
        prompt_dict = self.build_prompt(prompt)

        # Create ids for the messages
        prompt_id = self.next_id
        self._next_id()
        response_id = self.next_id
        self._next_id()
        
        # Create User prompt bubbles
        user_message = UserContainer(info=prompt_dict, message_id=prompt_id)
        user_message.setText(prompt)

        # Create Row for user container
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, self._chat_area.conversation.HORIZONTAL_MARGIN, 0)
        row.addStretch()
        row.addWidget(user_message)

        # Insert User Message
        self._conversation.mlayout.insertLayout( self._conversation.mlayout.count() - 1, row)

        #Auto scroll to maximum
        bar = self._conversation.scroll_area.verticalScrollBar()
        bar.setValue(bar.maximum())

        # Create a text bubble for the response
        assistant_message = BotContainer(info=prompt_dict, message_id=response_id)
        assistant_message.setText("")

        # Initialize a new worker with the model name and prompt (input)
        worker = ResponseWorker(prompt_dict, self.toolController, prompt_id)

        # Connnect signal to update the prompt display
        worker.signals.update_prompt_display.connect(self.updatePromptDisplay)

        # PROCESS CHUNK take a single chunk and handle it into the resopnse bubble
        #Connect the workers chunk signal to the handle chunk function
        worker.signals.process_chunk.connect(lambda chunk: self._handle_chunk(assistant_message, chunk))

        # STOP the worker has completed its work and the response has been streamed
        #Connect the workers stop signal to the finish response function
        worker.signals.stop.connect(lambda: self._finalize_response(prompt))

        QThreadPool.globalInstance().start(worker) #start

    # Streams the current chunk to the response bubble in the conversation window
    # This also catches each chunk so that the entire message can be saved
    def _handle_chunk(self, assistant_message: BotContainer, chunk: str):
        
        # Add chunk to temporary storage
        self.last_response.append(chunk)

        # If the response bubble is empty we need to do some handling to get it in the correct 
        # position and ready for streaming
        if assistant_message.toPlainText() == "":
            # Define a row for custom spacing
            row = QHBoxLayout()
            row.setContentsMargins(self._chat_area.conversation.HORIZONTAL_MARGIN, 0, 0, 0)
            row.addWidget(assistant_message)
            row.addStretch()

            # finally add it to the layout 
            self._conversation.mlayout.insertLayout(self._conversation.mlayout.count() - 1, row)

        # Add the current chunk to the previous text in the bubble
        text = assistant_message.toPlainText() + chunk

        #Set the bubble text to the new full response
        assistant_message.setText(text)

        # Auto scroll the conversation area to the bottom
        bar = self._conversation.scroll_area.verticalScrollBar()
        bar.setValue(bar.maximum())

    # Finalize the response by adding it to the memory manager and clearing the temporary chunk collection
    def _finalize_response(self, prompt: str):
        #Add to conversation history
        self.memManager.addMessage(prompt, "".join(self.last_response))

        #print(self.memManager.getRecent())
        self.last_response = [] # Clear the temporary collection

        # Reset active prompt check
        self.ACTIVE_PROMPT = False

    # On a worker signal updates the token count state for a prompt in the display area
    def updatePromptDisplay(self, message_id, info):
        bubble_name = "bubble"+str(message_id)
        roi = self._conversation.findChild(UserContainer, bubble_name)
        roi.update_tokens(info)

    # Updates the Memory Manager to have a new contect window
    # The `recent` field is rebuild with a length of the last `newWindow` messages
    def updateWindowSize(self, newWindow: int):
        self.memManager.rebuild_deque(newWindow)

        # Builds a list of  currently active tools that can be attached directly to the prompt
    
        # Sets a reference dict with tool names as keys and references to their ui 
    
    # toggle elements as keys
    def setToolToggleRefrences(self, reference_dict: dict):
        self.active_tools = reference_dict
    
    # Returns a list of the tools that are currently active based on the refrence list
    def getActiveTools(self):

        tools = []

        # iterate over tools
        for key, value in self.active_tools.items():
            
            # check reference value to see if its selected
            if value.get_status():
                tools.append(self.TOOL_REGISTRY[key])

        return tools

    # Returns a list of the tools that can be used
    def getTools(self):
        return self.AVAILABLE_TOOLS
    
    # Returns a list of models available for ollama to use
    def getModels(self):
        return list(self.models)
    
    # Deletes the last prompt message pair from mem manager and screen
    def undo(self):

        count = self._conversation.mlayout.count()
        #print("Count before ", count)

        # When the latest prompt response pair is complete count will always be odd.
        if not count > 1:
            return
        
        #CLear from memory
        self.memManager.undo()

        #Most recent item
        #print(self._conversation.mlayout.itemAt(count-2))
        if isinstance(self._conversation.mlayout.itemAt(count-2), QHBoxLayout):
            clear_layout(self, self._conversation.mlayout.itemAt(count-2))
            self._conversation.mlayout.takeAt(count-2)
            count -= 1
        #print("Count between ", self._conversation.mlayout.count())
        # Second most recent aka the new most recent
        #print(self._conversation.mlayout.itemAt(count-2))
        if isinstance(self._conversation.mlayout.itemAt(count-2), QHBoxLayout):
            clear_layout(self, self._conversation.mlayout.itemAt(count-2))
            self._conversation.mlayout.takeAt(count-2)

        #print("Count after ", self._conversation.mlayout.count())

    # Performs a clear of the Memory Manager wiping all data, performs a iterive 
    # clear of the conversation window erasing all messages
    def clearMemory(self):
        self.memManager.clear()

        print("Count before ", self._conversation.mlayout.count())

        #Delete chats
        print(self._conversation.mlayout.count())
        for i in reversed(range(self._conversation.mlayout.count())): 
            if isinstance(self._conversation.mlayout.itemAt(i), QHBoxLayout):
                #Clears the sublayout of the message
                clear_layout(self, self._conversation.mlayout.itemAt(i))
                #Finally remove for good
                self._conversation.mlayout.takeAt(i)

        print("Count after ", self._conversation.mlayout.count())
    
    # Iterated the message id
    def _next_id(self):
        self.next_id += 1
    
    # Returns true is a prompt is running 0 if its complete
    def activePrompt(self):
        return self.ACTIVE_PROMPT
# <<< CHAT CONTROLLER <<<