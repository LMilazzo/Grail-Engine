from PyQt6.QtCore import QThread, QMetaObject, Qt, Q_ARG
from PyQt6.QtGui import QColor

from GUI.PromptArea import PromptArea
from GUI.ChatArea import ChatArea
from GUI.SideBar import SideBar

from Controllers.DataLoader import DataLoader
from Controllers.ChatController import ChatController
from Controllers.MemoryController import MemoryController
from Controllers.OllamaController import OllamaController
from Controllers.ToolController import ToolController
from Controllers.ModelRunner import ModelRunner
from Controllers.PlotController import PlotController

# >>> APP MEDIATOR >>>
class AppMediator():
    def __init__(self, PromptArea: PromptArea, ChatArea: ChatArea, SideBar: SideBar, DataLoader: DataLoader):

        #--------------------------------------------------  
        #------------------- UI OBJECTS -------------------
        #--------------------------------------------------
        self.PromptArea = PromptArea

        self.ChatArea = ChatArea

        self.SideBar = SideBar
        
        #--------------------------------------------------  
        #---------------- UI CONTROLLERS ------------------
        #--------------------------------------------------
        self.ChatController = ChatController(self.ChatArea)

        self.SideBarController = None

        self.PlotController = PlotController()

        #--------------------------------------------------  
        #-------------- LOGIC CONTROLLERS -----------------
        #--------------------------------------------------

        self.DataLoader = DataLoader

        self.MemoryController = MemoryController(window=12)

        self.ToolController = ToolController(self.DataLoader.getOllamaTools(), self.DataLoader.getToolKeys())

        self.OllamaController = OllamaController(self.ToolController)

        self.ModelRunner = ModelRunner()
        self.ModelRunnerThread = QThread()

        #--------------------------------------------------  
        #--------------- CONNECT SIGNALS-------------------
        #--------------------------------------------------
        
        # UI
        self.connectPromptAreaSignals()
        self.connectSideBarSignals()

        # CONTROLLER
        self.connectOllamaControllerSignals()
        self._init_ModelRunner()


#__________________________________________________________________________________________________________
    
    #--------------------------------------------------  
    #-------------- CONNECTION SETUPS -----------------
    #--------------------------------------------------
    def connectPromptAreaSignals(self):
        self.PromptArea.signals.prompt_requested.connect(self.handlePrompt)

    def connectOllamaControllerSignals(self):

        self.OllamaController.signals.chunk_return.connect(lambda c: self.ChatController.stream_to_latest_assistant(c))

        # CONNECT FIRST CHUNK SIGNAL TO INNITIALIZE RESPONSE
        self.OllamaController.signals.first_chunk.connect(lambda params: self.ChatController._init_Response(params))

        self.OllamaController.signals.stop.connect(lambda p, r: self.MemoryController.addMessage(p, r))
        self.OllamaController.signals.stop.connect(
            lambda p, r: 
            QMetaObject.invokeMethod(
                self.ModelRunner, 
                "runEmbedder", 
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, p), Q_ARG(str, r) 
            )
        )
        
        self.OllamaController.signals.prompt_update.connect(lambda p: self.ChatController.updateLatestPrompt(p))

    def connectSideBarSignals(self):

        self.SideBar.setPlot(self.PlotController.plot())

        self.SideBar.signals.clear_chat.connect(self.MemoryController.clear)
        self.SideBar.signals.clear_chat.connect(self.ChatController.clear)
        self.SideBar.signals.clear_chat.connect(lambda: self.SideBar.setPlot(self.PlotController.clear()))

        self.SideBar.signals.clear_last_chats.connect(self.MemoryController.undo)
        self.SideBar.signals.clear_last_chats.connect(self.ChatController.undo)
        self.SideBar.signals.clear_last_chats.connect(lambda: self.SideBar.setPlot(self.PlotController.clearLast()))

    def _init_ModelRunner(self):

        # CONNECT LOAD STATUS TO UI ELEMENT TO SHOW STATUS
        self.ModelRunner.signals.status_good.connect(lambda: self.ChatArea.updateShadow(QColor("#361f3d")))
        
        # CONNECT EMBEDDING MODEL TO MEMORY CONTROLLER
        self.ModelRunner.signals.embedder_return.connect(self.MemoryController.addEmbedded)
        
        # CONNECT EMBEDDING MODEL TO PLOTTING MODEL
        self.ModelRunner.signals.embedder_return.connect(
            lambda x:
            QMetaObject.invokeMethod(
                self.ModelRunner, 
                "runPlotReducer", 
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(dict, x["prompt"]), Q_ARG(dict, x["response"]) 
            )
        )

        # CONNECT PLOT REDUCER RETURN TO PLOT UPDATING
        self.ModelRunner.signals.plot_reducer_return.connect(
            lambda datalist: self.SideBar.setPlot(self.PlotController.addDataPlot(datalist))
        )

        self.ModelRunner.moveToThread(self.ModelRunnerThread)
        
        self.ModelRunnerThread.start()

        QMetaObject.invokeMethod(self.ModelRunner, "loadModels", Qt.ConnectionType.QueuedConnection)
       
#__________________________________________________________________________________________________________

    def handlePrompt(self, model: str, prompt: str):
        params = self.SideBar.getPromptRelavantData()
        params["model"] = model
        params["prompt"] = prompt

        self.ChatController.addPrompt(params)

        params["history"] = self.MemoryController.getRecent()

        params["tools"] = self.ToolController.getActiveToolFunctions(params["tools"])

        self.OllamaController.runPrompt(params)

    def placeholderFeature(self):
        print("This is a wonderful test feature yet to be implemented")


# <<< APP MEDIATOR <<<