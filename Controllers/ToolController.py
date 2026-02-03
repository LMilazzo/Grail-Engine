import random
from ToolRegistry.get_weather import get_weather
from ToolRegistry.tavily_search import tavily_search


# >>> TOOL EXECUTOR >>>
class ToolController():
    def __init__(self):
        pass

    # Processes a single tool request
    def process_request(self, tool_request):
        
        print("------------------------------------------------------------------------")
        print(f"\033[31m ++ PROCESSING TOOL REQUEST [{tool_request['id']}] [{tool_request['function']['name']}]\033[0m")
        print("------------------------------------------------------------------------")
        #fake_content = {"role": "tool", "tool_call_id": tool_request['id'], "content": f"{random.randint(1, 10)} degrees"}

        try:

            if tool_request["function"]["name"] == "get_weather":
                response = get_weather(tool_request)

            if tool_request["function"]["name"] == "search":
                response = tavily_search(tool_request)

        # There was most likely an error in request parsing
        except Exception as e:

            response = {
                "role": "tool",
                "tool_call_id": tool_request["id"],
                "content": f"ERROR: {str(e)}"
            }
        
        return  response
# <<< TOOL EXECUTOR <<<