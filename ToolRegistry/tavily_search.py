import json
import os

from tavily import TavilyClient

from ToolRegistry.find_args import *

#[
#   {
#       'id': 'call_6t9jj2rn', 
#       'function': {
#           'index': 0, 'name': 
#           'tavily_search', 
#           'arguments': {
#               'query': '...'
#           }
#       }
#   }
#]

# A System prompt type statement describing the use of the tool
TOOL_DESCRIPTION = """
search: 
- Use this tool when the user requests factual, current, or external information that cannot be reliably inferred without searching.  
- The data returned comes from a trusted search source and must be treated as authoritative.  
- Do not guess or fabricate information when search results are available.  
- Use this tool for topics involving real-world facts, names, dates, definitions, or references.  
- You may perform multiple search calls if the user’s request involves multiple distinct queries.  
- Each tool request should contain exactly one search query.  
"""

# A list of valid argument names that will be mutated to the key argument
ARG_MAP = {
    "query": ["query", "search", "message", "content", "text"]
}


def tavily_search(payload: dict):

    print(f"\033[35m Payload: {json.dumps(payload, indent=4)}\033[0m")

    # Handle Args
    args = find_args(payload["function"]["arguments"], ARG_MAP)
    query = args["query"]

    # Get API key from env
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        raise RuntimeError("API key not set")

    tavily_client = TavilyClient(api_key=key)
    tavily_response = tavily_client.search(query, max_results=20, include_answer='advanced')

    #Parse relavant result info
    results_scores = {}
    for result in tavily_response["results"]:
        results_scores[result["score"]] = {"url" : result["url"], "content" : result["content"]}

    # Sort by relevance score
    results_sorted = dict(sorted(results_scores.items()))

    # Take 3 most relevant items
    top3 = sorted(results_sorted.items(), key=lambda x: x[0], reverse=True)[:3]

    results = []
    for item in top3:
        res = {
            "url" : result["url"],
            "relavant_content": result["content"]
        }
        results.append(res)

    response_content = {
        "query" : query ,
        "query_answer" : tavily_response["answer"],
        "sources" : results
    }

    response = {
        "role": "tool",
        "tool_call_id": payload["id"],
        "content": f"{json.dumps(response_content, indent=4)}"
    }

    return response