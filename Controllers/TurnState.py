import json

# >>> TURN STATE >>>
class TurnState():
    def __init__(self, prompt_payload):
        
        # ORIGINAL PROMPT
        self.payload = prompt_payload

        # MESSAGE LIST
        self.message_list = prompt_payload["messages"]

        # THE MOST RECENT RESPONSE
        self.last_response = ""

#__________________________________________________________________________________________________________

    # Adds a message to the propmt message list
    def _add_message(self, message):
        self.message_list.append(message)
        self.payload["messages"] = self.message_list

    # Returns the payload
    def getPayload(self):
        return self.payload
    
    def setLastResponse(self, response):
        self.last_response = response
    
    def getLastResponse(self):
        return self.last_response
#__________________________________________________________________________________________________________

    # Adds a whole list of requests to the message list
    def addToolRequests(self, request_list):
        #print("adding")
        message = {"role" : "assistant", "tool_calls" : request_list}
        #print(message)
        self._add_message(message)

    # Adds a tool response to the message list
    def addToolResponse(self, tool_response):
        self._add_message(tool_response)
#__________________________________________________________________________________________________________

    def print(self):
        print(json.dumps(self.payload, indent=2))
        return self.payload
# <<< TURN STATE <<<