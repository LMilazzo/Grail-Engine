import pandas as pd
import json

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
        
#__________________________________________________________________________________________________________

    def getModels(self):
        return self.models
    
    def getPresets(self):
        return self.presets
    
    def getOllamaTools(self):
        return self.ollama_tools
    
    def getToolKeys(self):
        return self.tool_keys

    
# <<< DATA LOADER <<<