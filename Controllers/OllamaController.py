from PyQt6.QtCore import QObject, pyqtSignal, QThreadPool
from PyQt6.QtWidgets import *

from Controllers.PromptBuilder import PromptBuilder
from Controllers.OllamaWorker import OllamaWorker
from Controllers.ToolController import ToolController

#**************  SIGNALS *****************
class ControllerSignals(QObject):
    chunk_return = pyqtSignal(str)
    stop = pyqtSignal(str, str)
    prompt_update = pyqtSignal(dict)
    first_chunk = pyqtSignal(dict)
#**************  SIGNALS *****************


# >>> OLLAMA CONTROLLER >>>
class OllamaController():
    def __init__(self, ToolController: ToolController):
        
        #**************  SIGNALS *****************
        self.signals = ControllerSignals()

        self.ToolController = ToolController

        self.current_response = []

#__________________________________________________________________________________________________________

    def runPrompt(self, params):

        # BUILD PROMPT
        prompt_builder = PromptBuilder(params)

        initial_prompt = prompt_builder.build()

        worker = OllamaWorker(initial_prompt, params, self.ToolController)

        worker.signals.process_chunk.connect(lambda chunk: self._emit_chunk(chunk, params))

        worker.signals.stop.connect(lambda: self.finished(params["prompt"]))

        worker.signals.final_prompt.connect(self._emit_final_prompt)

        QThreadPool.globalInstance().start(worker)
        

    def _emit_chunk(self, chunk, params):
        self.current_response.append(chunk)
        
        # THIS IS THE FIRST CHUNK acknowledge that and send a signals
        if len(self.current_response) == 1:
            self.signals.first_chunk.emit(params)
            
        self.signals.chunk_return.emit(chunk)

    def _emit_final_prompt(self, prompt):
        self.signals.prompt_update.emit(prompt)

    def finished(self, prompt):
        self.signals.stop.emit(prompt, "".join(self.current_response))
        self.current_response = []


# <<< OLLAMA CONTROLLER <<<