from PyQt6.QtCore import QObject, pyqtSignal

from collections import deque

import random
import json
import os

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
# LOGGING

    # Create a new log file
    def newLog_init_(self):

        random_seed = str(random.randint(0, 999999999))
                
        open(LOG_BASE_PATH+random_seed+".jsonl", "w").close()

        self.signals.new_log_created.emit(random_seed)

        self.ACTIVE_LOG = random_seed

    def writeToLog(self, item: dict):

        with open(f"{LOG_BASE_PATH}{self.ACTIVE_LOG}.jsonl", "a") as log:
            log.write(json.dumps(item) + "\n")
    
    def changeActiveLog(self, new_active: str):
        print("Changing log to [", new_active, "]")
        self.ACTIVE_LOG = new_active

    def loadMemoryFromLog(self):
        print(f"\033[31m _____________________________________________________ \033[0m")
        print(f"\033[31m Loading Memory \033[0m")

        msgs = []

        with open(f"{LOG_BASE_PATH}{self.ACTIVE_LOG}.jsonl") as f:
            for line in f:
                item = json.loads(line)
                self.history.append(item)
                self.recent.append(item)
        
        print(f"\033[31m Loaded: {len(self.history)} Total Messages - {len(self.recent)} In Window \033[0m")


        print(f"\033[31m _____________________________________________________ \033[0m")

        self.signals.log_memory_loaded.emit(self.history)

    def undoLog(self):
        with open(f"{LOG_BASE_PATH}{self.ACTIVE_LOG}.jsonl", "rb+") as f:

            # DELETE LAST LOG ENTRY
            f.seek(0, os.SEEK_END)
            end = f.tell()

            if end == 0:
                # empty file
                pass
            else:
                pos = end - 1

                # Skip trailing newline(s)
                while pos >= 0:
                    f.seek(pos)
                    if f.read(1) != b"\n":
                        break
                    pos -= 1

                # Find the previous newline
                while pos >= 0:
                    f.seek(pos)
                    if f.read(1) == b"\n":
                        break
                    pos -= 1

                # Truncate
                if pos >= 0:
                    f.truncate(pos + 1)
                else:
                    # Only one line in file
                    f.truncate(0)

    def clearLog(self):

        #ERASE ALL DATA
        with open(f"{LOG_BASE_PATH}{self.ACTIVE_LOG}.jsonl", "r+") as f:
            f.truncate(0)
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

        # CLEAR LOG FILE
        self.clearLog()

    #Deletes the last messege prompt pair
    def undo(self):

        # REMOVE LAST MESSAGE FROM LIST
        self.history = self.history[:-1]

        self.history_embedded = self.history_embedded[:-1]

        # REBUILD WITH THE CORRECT ITEMS
        self.rebuild_deque(self.window)

        # UNDO LOG LAST LINE
        self.undoLog()

# <<< CONVERSATION  HISTORY <<<