from PyQt6.QtCore import QObject, pyqtSignal

from Utils.OllamaUtils import * 

from Controllers.TurnState import TurnState
from Controllers.ToolController import ToolController

import time
import json


#**************  SIGNALS *****************
class ControllerSignals(QObject):
    final_prompt = pyqtSignal(dict)
#**************  SIGNALS *****************


# >>> TURN CONTROLLER >>>
class TurnController(QObject):
    def __init__(self, Turn_State: TurnState, Tool_Controller: ToolController):
        super().__init__()

        #**************  SIGNALS *****************
        self.signals = ControllerSignals()

        # Turn state object for prompt handling
        self.TurnState = Turn_State

        # The tool controller hub
        self.ToolController = Tool_Controller

#__________________________________________________________________________________________________________

    def agent_loop(self):
        
        while True:

            # 1.) Execute Prompt
            self._execute_prompt()
            response = self.TurnState.getLastResponse()

            #2.) Check For Tool Requests
            #tool_requests = self._is_tool_calls(self.TurnState.getLastResponse())
            assistant_buffer = ""

            for line in response.iter_lines(decode_unicode=True):

                if not line:
                    continue

                data = json.loads(line)

                #--------------------------------------------------  
                #---------------- STREAM CONTENT ------------------
                #--------------------------------------------------
                # 1. Stream content
                if "message" in data and "content" in data["message"]:
                    chunk = data["message"]["content"]
                    assistant_buffer += chunk
                    yield {"type": "content", "data": chunk}

                #--------------------------------------------------  
                #-------------- IF TOOL REQUESTS ------------------
                #--------------------------------------------------
                # 2. Tool call interrupt
                if "message" in data and "tool_calls" in data["message"]:
                    tool_requests = data["message"]["tool_calls"]

                    print(f"\033[33mTOOLS REQUESTED\033[0m")
                    print("------------------------------------------------------------------------")
                    print(f"\033[33m-Tool Calls-\033[0m")
                    print(tool_requests)
                    for x in tool_requests:
                        print(f"\033[33m  +  ID: {x['id']} \033[0m")
                        print(f"\033[33m    -  Function: {x['function']['name']} \033[0m")
                        print(f"\033[33m    -  Params: {x['function']['arguments']} \033[0m")
                    print("------------------------------------------------------------------------")

                    self.TurnState.addToolRequests(tool_requests)

                    for request in tool_requests:
                        tool_response = self.ToolController.processRequest(request)
                        self.TurnState.addToolResponse(tool_response)

                    break  #Break and re-stream

                #--------------------------------------------------  
                #-------------------- COMPLETION ------------------
                #--------------------------------------------------
                # 3. Proper completion handling
                if data.get("done") is True:
                    self.TurnState._add_message({
                        "role": "assistant",
                        "content": assistant_buffer
                    })
                    
                    print("------------------------------------------------------------------------")
                    print(f"\033[32m \n\n Final Prompt \033[0m")
                    self.TurnState.print()
                    print("------------------------------------------------------------------------")

                    # EMIT SIGNAL WITH THE FINAL PROMPT
                    self.signals.final_prompt.emit(self.TurnState.getPayload())

                    return  # EXIT ENTIRE agent_loop()
            
#__________________________________________________________________________________________________________  
 
    # Sends a prompt to the Ollama API/Chat using ollamaPrompt from OllamaUtils
    def _execute_prompt(self):
        response = ollamaPrompt(payload=self.TurnState.getPayload(), stream=True)
        self.TurnState.setLastResponse(response)

    # Returns the final response from the loop
    def getResponse(self):
        return self.TurnState.getLastResponse()

# <<< TURN CONTROLLER <<<