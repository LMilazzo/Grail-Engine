import requests
import json

URL = "http://localhost:11434/api/"

# >>> OLLAMA REQUEST >>>
def ollamaPrompt(payload, url="http://localhost:11434/api/chat"):

    response = requests.post(url, json=payload, stream=False)

    return response
# <<< OLLAMA REQUEST <<<


# >>> OLLAMA STREAM RESPONSE >>>
def streamResponse(response):

    for line in response.iter_lines(decode_unicode=True):
        if line: # Ignore empty lines
            try:    
                j = json.loads(line)
                #Find response token
                if "message" in j and "content" in j["message"]: 
                    #print(j["message"]["content"], end="")
                    yield j["message"]["content"]

            except json.JSONDecodeError:
                yield f"failed to parse line {line}"
# <<< OLLAMA STREAM RESPONSE <<<


# >>> LIST MODELS >>>
def listModels(url = "http://localhost:11434/api/tags"):
    
    response = requests.get(url)

    modelList = []

    if response:

        try:
            j = response.json()

            #If models 
            if "models" in j:
                for m in j["models"]:
                    modelList.append(m["name"])
            else:
                print(f"Failed to retrieve models from {response}")
                return []
            
        except json.JSONDecodeError:
            print(f"Failed to retrieve models from {response}")
            return []
    
    return modelList
# <<< LIST MODELS <<<

# >>> GET TOKEN COUNT FROM PROMPT >>> 
def TokenCountEstimate_Prompt(payload):

    chars = sum(len(m["content"]) for m in payload["messages"] if "content" in m)
    
    token_rough_estimate = chars // 4

    overhead_estimate = len(payload["messages"]) * 8

    return token_rough_estimate + overhead_estimate
# <<< GET TOKEN COUNT <<<

# >>> GET TOKEN COUNT FROM STRING >>> 
def TokenCountEstimate_String(payload):

    chars = len(payload)
    
    token_rough_estimate = chars // 4

    return token_rough_estimate
# <<< GET TOKEN COUNT <<<

