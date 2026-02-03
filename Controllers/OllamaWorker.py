from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool

from Controllers.TurnController import *

from Utils.OllamaUtils import * 

import time
import json

# >>> WORKER SIGNALS >>>s
class WorkerSignals(QObject):
    process_chunk = pyqtSignal(str)
    stop = pyqtSignal()
    update_prompt_display = pyqtSignal(int, dict)
# <<< WORKER SIGNALS <<<


# >>> WORKER >>>
class ResponseWorker(QRunnable):
    def __init__(self, prompt: dict, toolController: "ToolController", prompt_id: int):
        super().__init__()
        
        self.payload = prompt # A Prompt object
        self.signals = WorkerSignals()

        # The tool controller hub
        self.toolController = toolController

        #The id of the prompt
        self.prompt_id = prompt_id

    def run(self):
        # Builds some classes that 
        # - send the prompt
        # - intercept response
        # - call tools
        # - rebuild prompt if necessary
        # - repeat until no tool calls
        # - return resopnse stream
        # Call stream to stream results
        turn_state = TurnState(self.payload)
        turn_controller = TurnController(turn_state, self.toolController, self.prompt_id)
        turn_controller.signals.update_prompt_display.connect(self.updatePromptDisplay)

        response_stream = turn_controller.agent_loop()

        if response_stream:
            self._stream(response_stream)

    def _stream(self, response_stream):
        for chunk in streamResponse(response_stream):
            self.signals.process_chunk.emit(chunk)  #Emit chunk to conversation
            time.sleep(0.02)
        self.signals.stop.emit() #Emit the final signal ending the response

    def updatePromptDisplay(self, id, payload):
        #Update Prompt bubble signal
        self.signals.update_prompt_display.emit(id, payload)
# <<< WORKER <<<