import json

from ToolRegistry.find_args import *

#[
#   {
#       'id': 'call_6t9jj2rn', 
#       'function': {
#           'index': 0, 'name': 
#           'get_weather', 
#           'arguments': {
#               'location': 'Rutland Vermont'
#           }
#       }
#   }
#]

# A System prompt type statement describing the use of the tool
TOOL_DESCRIPTION = """
get_weather: 
- Use this tool when the user requests weather data for a specific location. 
- The data returned comes from a reliable weather api and must not be questioned. 
- Each tool request should contain exactly one location.  
"""

# A list of valid argument names that will be mutated to the key argument
ARG_MAP = {
    "location": ["location", "place", "city", "town", "query"]
}


def get_weather(payload: dict):

    print(f"\033[35m Payload: {json.dumps(payload, indent=4)}\033[0m")

    args = find_args(payload["function"]["arguments"], ARG_MAP)

    location = args["location"]

    response = {
        "role": "tool",
        "tool_call_id": payload["id"],
        "content": f"{location}: 32°F, light rain."
    }

    return response