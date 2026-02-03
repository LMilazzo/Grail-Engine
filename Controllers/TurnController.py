from PyQt6.QtCore import QObject, pyqtSignal

from Utils.OllamaUtils import * 

from Controllers.TurnState import TurnState

import time
import json


# >>> CONTROLLER SIGNALS >>>
class TurnControllerSignals(QObject):
    # Signal to update the token count or stats regarding the prompt
    update_prompt_display = pyqtSignal(int, dict)
# <<< CONTROLLER SIGNALS <<<


# >>> TURN CONTROLLER >>>
class TurnController(QObject):
    def __init__(self, turnState: TurnState, toolController: "ToolController", prompt_id: int):
        super().__init__()

        # Turn state object for prompt handling
        self.turn_state = turnState

        # The tool controller hub
        self.toolController = toolController

        # The id of the prompt user message
        self.prompt_id = prompt_id

        self.signals = TurnControllerSignals()

    def agent_loop(self):
        
        while True:
            # 1.) Execute Prompt
            self._execute_prompt()

            # 2.) Check For Tool Requests
            tool_requests = self._is_tool_calls(self.turn_state.getLastResponse())

            # 3.) If There Is Tool Requests...
            if tool_requests:

                print(f"\033[33mTOOLS REQUESTED\033[0m")
                print(f"\033[33m{tool_requests}\033[0m")

                # 4.) Add Tool Requests To The Turn State
                self.turn_state.add_tool_requests(tool_requests)

                # DEBUGGING PRINTING
                print("------------------------------------------------------------------------")
                print(f"\033[33m-Tool Calls-\033[0m")
                print(tool_requests)
                for x in tool_requests:
                    print(f"\033[33m  +  ID: {x['id']} \033[0m")
                    print(f"\033[33m    -  Function: {x['function']['name']} \033[0m")
                    print(f"\033[33m    -  Params: {x['function']['arguments']} \033[0m")
                print("------------------------------------------------------------------------")

                # 5.) For Each Tool Request Resolve It And Add To Turn State
                for x in tool_requests:

                    # Resolve the request
                    content = self.toolController.process_request(x)

                    self.turn_state.add_tool_response(content)

            # 3.) If There Is Not Tool Requests Return The Response
            else:
                print("------------------------------------------------------------------------")
                print(f"\033[32mPROCEEDING TO STREAM \n\n Final Prompt \033[0m")

                #Send signal to update prompt
                self.updatePromptDisplay()

                self.turn_state.print()
                print("------------------------------------------------------------------------")
                return self.getResponse()
        
    # Sends a prompt to the Ollama API/Chat using ollamaPrompt from OllamaUtils
    def _execute_prompt(self):
        response = ollamaPrompt(payload=self.turn_state.getPayload())
        self.turn_state.setLastResponse(response)

    # Returns the final response from the loop
    def getResponse(self):
        return self.turn_state.getLastResponse()

    # Determine if there was any tool calls needed from the response
    def _is_tool_calls(self, response):
        tool_reqs = []
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    j=json.loads(line)
                    #Find response token
                    if "message" in j and "tool_calls" in j["message"]: 
                        tool_reqs = j["message"]["tool_calls"]
                        return j["message"]["tool_calls"]
                    else:
                        return None

                except json.JSONDecodeError:
                    return f"failed to parse line {line}"
    
    # Updates the token count on the prompt bubble to include any tools or prompt changes 
    def updatePromptDisplay(self):
        self.signals.update_prompt_display.emit(self.prompt_id, self.turn_state.getPayload())
# <<< TURN CONTROLLER <<<