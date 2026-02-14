from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool


from Controllers.ToolController import ToolController
from Controllers.TurnController import TurnController
from Controllers.TurnState import TurnState

from Utils.OllamaUtils import * 

import time
import json

#**************  SIGNALS *****************
class WorkerSignals(QObject):
    process_chunk = pyqtSignal(str)
    stop = pyqtSignal()
    final_prompt = pyqtSignal(dict)
#**************  SIGNALS *****************


# >>> WORKER >>>
class OllamaWorker(QRunnable):
    def __init__(self, initial_prompt: dict, params: dict, toolController: ToolController):
        super().__init__()
        
        #**************  SIGNALS *****************
        self.signals = WorkerSignals()


        self.payload = initial_prompt

        self.toolController = toolController

        self.params = params
#__________________________________________________________________________________________________________

    def run(self):
        # Builds some classes that 
        # - send the prompt
        # - intercept response
        # - call tools
        # - rebuild prompt if necessary
        # - repeat until no tool calls
        # - return resopnse stream
        # Call stream to stream results
        Turn_State = TurnState(self.payload)

        Turn_Controller = TurnController(Turn_State, self.toolController)

        # CONNECT FINAL PROMPT SIGNALS
        Turn_Controller.signals.final_prompt.connect(self.emitFinalPrompt)

        response_stream = Turn_Controller.agent_loop()

        if response_stream:
            self._stream(response_stream)

    def _stream(self, response_stream):
        for chunk in response_stream: #streamResponse(response_stream):
            self.signals.process_chunk.emit(chunk["data"])  #Emit chunk to conversation
            #time.sleep(0.02)
        self.signals.stop.emit() #Emit the final signal ending the response

    def emitFinalPrompt(self, final_prompt):
        self.signals.final_prompt.emit(final_prompt)

# <<< WORKER <<<