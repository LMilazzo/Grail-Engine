from PyQt6.QtCore import QObject, pyqtSignal

from collections import deque

import random
import json

# >>> CONTROLLER SIGNALS >>>
class ControllerSignals(QObject):
    # Signal
    new_log_created = pyqtSignal(str)
    log_memory_loaded = pyqtSignal(list)
# <<< CONTROLLER SIGNALS <<<

LOG_BASE_PATH = "HISTORY/LOGS/"

# >>> CONVERSATION MEMORY >>>
class MemoryController():
    def __init__(self, window: int):

        #**************  SIGNALS *****************
        self.signals = ControllerSignals()

        # Message Window
        self.window = window

        #--------------------------------------------------  
        #-------------- MESSAGES IN WINDOW ----------------
        #--------------------------------------------------
        self.recent = deque(maxlen=window)

        #--------------------------------------------------  
        #----------------- FULL HISTORY -------------------
        #--------------------------------------------------
        # **PRIMITIVE**
        self.history = []

        #--------------------------------------------------  
        #----------------- FULL HISTORY -------------------
        #--------------------------------------------------
        self.history_embedded = []

        #--------------------------------------------------  
        #-------------- CURRENT FILE NAME------------------
        #--------------------------------------------------
        self.ACTIVE_LOG = None

#__________________________________________________________________________________________________________
    
    def addMessage(self, prompt: str, response: str):
        
        #STRUCTURE{prompt: "str", response: "str"}
        item = {"prompt": prompt, "response": response}

        self.recent.append(item)
        self.history.append(item)
        
        self.writeToLog(item)

    # Returns a list of the x most recent messages
    def getRecent(self):
        return list(self.recent)
    
    def addEmbedded(self, items: dict):
        item1 = items["prompt"]
        item2 = items["response"]
        self.history_embedded.append(item1)
        self.history_embedded.append(item2)

#__________________________________________________________________________________________________________

    # Create a new log file
    def newLog_init_(self):

        random_seed = str(random.randint(0, 999999999))
                
        open(LOG_BASE_PATH+random_seed+".jsonl", "w").close()

        self.signals.new_log_created.emit(random_seed)

        self.ACTIVE_LOG = random_seed

    def writeToLog(self, item: dict):

        with open(LOG_BASE_PATH+self.ACTIVE_LOG+".jsonl", "a") as log:
            log.write(json.dumps(item) + "\n")
    
    def changeActiveLog(self, new_active: str):
        print("Changing log to [", new_active, "]")
        self.ACTIVE_LOG = new_active

    def loadMemoryFromLog(self):
        self.signals.log_memory_loaded.emit([])
#__________________________________________________________________________________________________________

    # Rebulds the recent messages deque with a new window size from the full conversation history
    def rebuild_deque(self, window: int):
        # CLEAR THE DEQUEUE
        self.recent.clear() 

        # REBUILD
        self.recent = deque(self.history[-window:], maxlen=window)

        # SET NEW WINDOW
        self.window = window

#__________________________________________________________________________________________________________

    # Clears the Memory manager fields for a fresh start
    def clear(self):

        self.recent.clear()

        self.history = []

        self.history_embedded = []

    #Deletes the last messege prompt pair
    def undo(self):

        # REMOVE LAST MESSAGE FROM LIST
        self.history = self.history[:-1]

        self.history_embedded = self.history_embedded[:-1]

        # REBUILD WITH THE CORRECT ITEMS
        self.rebuild_deque(self.window)

# <<< CONVERSATION  HISTORY <<<