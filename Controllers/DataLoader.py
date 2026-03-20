import pandas as pd
import json
import os

from Utils.OllamaUtils import listModels
from Model_Presets.Param_Presets import PARAM_PRESETS
from ToolRegistry.Registry import OLLAMA_TOOLS, AVAILABLE_TOOLS

# >>> DATA LOADER >>>
class DataLoader():
    def __init__(self):
       
        #---------------------------------------------
        #------------------ MODELS ------------------- 
        #---------------------------------------------
        self.models = listModels()

        #---------------------------------------------
        #----------------- PRESETS ------------------- 
        #---------------------------------------------
        self.presets = PARAM_PRESETS

        #---------------------------------------------
        #----------------- TOOLS --------------------- 
        #---------------------------------------------
        self.tool_keys = AVAILABLE_TOOLS
        self.ollama_tools = OLLAMA_TOOLS

        #---------------------------------------------
        #------------ PREVIOUS CHATS -----------------
        #---------------------------------------------
        self.logs = None
        
#__________________________________________________________________________________________________________

    def getModels(self):
        return ["llama3.1:8b"]#self.models 
    
    def getPresets(self):
        return self.presets
    
    def getOllamaTools(self):
        return self.ollama_tools
    
    def getToolKeys(self):
        return self.tool_keys
    
    def getLogs(self):
        return self.logs

    def pullLogs(self):
        l = os.listdir("HISTORY/LOGS")
        self.logs = l
        return l
    
# <<< DATA LOADER <<<