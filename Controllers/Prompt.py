from ToolRegistry.TOOL_STATEMENT import TOOL_STATEMENT

# >>> PROMPT >>>
class Prompt():
    
    # __init__
    def __init__(self, model: str, text: str, system: str, 
        temp=0.9, topP=0.9, repeat=0.0, topK=0.0, max_tokens=1024):
        
        # The user prompt / current message
        self.user = text

        # Model to use
        self.model = model

        # Tool handling
        self.tool_models = ["llama3.1:8b-instruct-q6_K", "qwen2.5:7b" ]
        self.use_tools = self.model in self.tool_models
        
        # The system prompt if the system prompt is empty it is ignored
        # This will also help the performance of models with system prompts defined in model files 
        if len(system) > 0:
            self.system = system
        else:
            self.system = None

        # Other Params
        self.temp = temp
        self.topP = topP
        self.repeat = repeat
        self.topK = topK
        self.max_tokens = max_tokens

        #The short term conversation history usually last x mesages
        self.conversation_history = []

        # A list of active tools
        self.tools = []

        # The Payload for the prompt
        self.payload = {}
        self.buildStatus = False

    # Returns the user prompt
    def getUserPrompt(self):
        return self.user
    
    # Sets the System prompt
    def editSystem(self, s):
        self.system = s
    
    # Returns the system prompt 
    def getSystem(self):
        return self.system

    # Sets the conversation history for the prompt
    def editConvHistory(self, h: list):
        self.conversation_history = h

    # Returns the conversation history
    def getConvHistory(self):
        return self.conversation_history

    # Sets the tools list 
    def setTools(self, tools: list):
        self.tools = tools
        
    # Uses the pieces of the prompt object to build a properly structured `meesages` list
    # for the ollama api/chat endpoints prompt
    def build(self):

        # #Messages list      
        messages = []

        # Add a system prompt is available
        if self.system:
            messages.append({"role" : "system", "content" : self.system})

        # If tools are allowed add the info usage rules
        if self.use_tools:
            messages.append({"role" : "system", "content": TOOL_STATEMENT})

        # Iterively add the conversation history to the messages list
        for i in self.conversation_history:
            user_prompt = {"role" : "user", "content" : i["prompt"]}
            assistant_response = {"role" : "assistant", "content" : i["response"]}
            messages.append(user_prompt)
            messages.append(assistant_response)
        
        # Finally add the current active user prompt
        messages.append({"role": "user", "content": self.user})
        
        #------------------------------------------------------------------------
        #Debug print parameters
        print(f"""------------------------------------------------------------------------\n\033[32m-Building Prompt\033[0m-\nTemp: {self.temp}\nTop P: {self.topP}\nRepeat: {self.repeat}\nTop K: {self.topK}\nTokens: {self.max_tokens}\nModel: {self.model}\nSystem: {self.system if self.system else ""}\n------------------------------------------------------------------------""")
        print("\033[32m-Previous History-\033[0m")
        for i in messages:
            if i["role"] == "user":
                print(f"\033[34m{i}\033[0m")
            else:
                print(f"\033[31m{i}\033[0m")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #------------------------------------------------------------------------
        
        # Models capable of using tools
        if self.use_tools:

            # Full Prompt
            self.payload = {
                "model" : f"{self.model}",
                "messages" : messages,
                "options": {
                    "temperature": self.temp,
                    "top_p": self.topP,
                    "top_k": self.topK,
                    "repeat_penalty": self.repeat,
                    "num_predict": self.max_tokens,
                },
                "tools" : self.tools
            }

        else: #Ignore the tools

            # Full Prompt
            self.payload = {
                "model" : f"{self.model}",
                "messages" : messages,
                "options": {
                    "temperature": self.temp,
                    "top_p": self.topP,
                    "top_k": self.topK,
                    "repeat_penalty": self.repeat,
                    "num_predict": self.max_tokens,
                }
            }


        self.buildStatus = True
        return self.payload
# <<< PROMPT <<<