from collections import deque

from Controllers.Prompt import * 
from Controllers.OllamaWorker import *

# >>> CONVERSATION MEMORY >>>
class MemoryManager():

    # __init__
    def __init__(self, window: int):

        self.window = window

        #List of recent messages and responses
        self.recent = deque(maxlen=window)

        #List of the full conversation
        self.history = []

    # Add the most recent prompt / response pair to the recent and full historys 
    def addMessage(self, prompt: str, response: str):
        
        #STRUCTURE{
        #   prompt: "str",
        #   response: "str"
        #}
        item = {
            "prompt": prompt,
            "response": response
        }

        self.recent.append(item)
        self.history.append(item)

    # Returns a list of the full conversation history
    def getHistory(self):
        return list(self.history)

    # Returns a list of the x most recent messages
    def getRecent(self):
        return list(self.recent)
    
    # Rebulds the recent messages deque with a new window size from the full conversation history
    def rebuild_deque(self, window: int):
        self.recent.clear() #clear the deque
        self.recent = deque(self.history[-window:], maxlen=window)
        self.window = window

    # Clears the Memory manager fields for a fresh start
    def clear(self):
        self.recent.clear()
        self.history = []

    #Deletes the last messege prompt pair
    def undo(self):

        # REmove last pair
        self.history = self.history[:-1]
        # Rebuild the deque without the last pair
        self.rebuild_deque(self.window)
# <<< CONVERSATION  HISTORY <<<