import json

# >>> TURN STATE >>>
class TurnState():
    def __init__(self, prompt_payload):
        
        # Original prompt
        self.payload = prompt_payload

        # List of messages
        self.message_list = prompt_payload["messages"]

        # The current most recent assistant response
        self.last_response = ""

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
    
    # Adds a whole list of requests to the message list
    def add_tool_requests(self, request_list):
        #print("adding")
        message = {"role" : "assistant", "tool_calls" : request_list}
        #print(message)
        self._add_message(message)

    # Adds a tool response to the message list
    def add_tool_response(self, tool_response):
        self._add_message(tool_response)

    def print(self):
        print(json.dumps(self.payload, indent=2))
        return self.payload
# <<< TURN STATE <<<