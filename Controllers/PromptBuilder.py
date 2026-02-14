
TOOL_STATEMENT = """
You are a tool-using assistant operating in a structured function-calling environment.

Your goal is to fully and accurately answer the user’s original request. If the request requires information that is not already available in the current conversation context, and a tool exists that can retrieve that information, you must call the appropriate tool. Do not guess or assume missing information when a tool can provide it.

If a tool call returns incomplete information and the user’s original request still cannot be answered with high confidence, you must call another relevant tool. Continue this process until either you have sufficient verified information to answer the user’s original request, or no available tool can provide additional relevant information.

Do not provide a final answer while required information is still missing and a suitable tool exists.

You must only call tools that are explicitly listed as available. Never invent or modify tool names. If no available tool can help, respond directly to the user without fabricating a tool.

When calling a tool, output only a valid structured tool call and nothing else. Do not include explanatory text alongside the tool call.

When you have gathered enough information to answer the user’s original request, stop calling tools and provide a clear, complete, and direct answer.
"""

# >>> PROMPT >>>
class PromptBuilder():
    def __init__(self, params: dict):
        
        #--------------------------------------------------  
        #-------------------- STATUS ----------------------
        #--------------------------------------------------
        self.buildStatus = False

        self.model = params["model"]

        #--------------------------------------------------  
        #----------------- TOOL STATUS --------------------
        #--------------------------------------------------
        self.tool_models = ["llama3.1:8b-instruct-q6_K", "qwen2.5:7b",]
        self.use_tools = self.model in self.tool_models
        # A list of active tools
        self.tools = params["tools"]

        #--------------------------------------------------  
        #----------------- PARAMETERS ---------------------
        #--------------------------------------------------
        #{
        #    "system": "",
        #    "temp": 0.9,
        #    "topP": 0.9,
        #    "topK": 40.0,
        #    "rep": 1.1,
        #    "tokens": 512,
        #    "tools": [],
        #    "model": "KURISU-1.5:latest",
        #   "prompt": "erfnjdfnkj",
        #    "id": 0,
        #    "token_estimate": 2
        #}
        self.text = params["prompt"]
        self.system = params["system"]
        
        # The system prompt if the system prompt is empty it is ignored
        # This will also help the performance of models with system prompts defined in model files 
        if len(self.system) < 1:
            self.system = None

        # Other Params
        self.temp = params["temp"]
        self.topP = params["topP"]
        self.repeat = params["rep"]
        self.topK = params["topK"]
        self.max_tokens = params["tokens"]

        #The short term conversation history usually last x mesages
        self.conversation_history = params["history"]

        # The Payload for the prompt
        self.payload = {}
#__________________________________________________________________________________________________________
        
    # Uses the pieces of the prompt object to build a properly structured `meesages` list
    # for the ollama api/chat endpoints prompt
    def build(self):

        #--------------------------------------------------  
        #----------------- MESSAGES ---------------------
        #--------------------------------------------------
        messages = []

        # SYSTEM MESSAGES
        if self.system and self.use_tools:
            self.system += TOOL_STATEMENT
            messages.append({"role" : "system", "content" : self.system})
        
        if not self.system and self.use_tools:
            self.system = TOOL_STATEMENT
            messages.append({"role" : "system", "content" : self.system})


        # CONVERSATION HISTORY
        for i in self.conversation_history:

            user_prompt = {"role" : "user", "content" : i["prompt"]}
            messages.append(user_prompt)


            assistant_response = {"role" : "assistant", "content" : i["response"]}
            messages.append(assistant_response)

        # CURRENT PROMPT
        messages.append({"role": "user", "content": self.text})
        
        self.debugPrint(messages)

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
        # Models capable of using tools
        if self.use_tools:
            self.payload["tools"] = self.tools

        #--------------------------------------------------  
        #-------------------- STATUS ----------------------
        #--------------------------------------------------
        self.buildStatus = True

        return self.payload
    
    def debugPrint(self, messages: list):
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

# <<< PROMPT <<<