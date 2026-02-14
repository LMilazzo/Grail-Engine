from ToolRegistry.get_weather import TOOL_DESCRIPTION as get_weather_statement
from ToolRegistry.tavily_search import TOOL_DESCRIPTION as tavily_search_statement

OLLAMA_TOOLS = {

# A tool to get the weather of a specific location
# takes a single location
"Get Weather" : {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": f"{get_weather_statement}",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get the weather from."
                }
            },
            "required": ["location"]
        }
    }
},

# A tool to use tavily to perform a single search query
"Search (Tavily)" : {
    "type": "function",
    "function": {
        "name": "search",
        "description": f"{tavily_search_statement}",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A search query to perform"
                }
            },
            "required": ["query"]
        }
    }
}

}

AVAILABLE_TOOLS = set(OLLAMA_TOOLS.keys())

