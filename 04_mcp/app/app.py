import argparse
import sys
from pathlib import Path

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters
from prompt_toolkit import prompt, HTML
from prompt_toolkit.completion import WordCompleter

from agent import ask_agent
from tools import get_weather
from utils import format_response

# Example travel topics for autocompletion
travel_completer = WordCompleter([
    "I love art and museums",
    "Looking for good food spots",
    "Find cheap flights to Tokyo",
    "Estimate daily budget in Amsterdam",
], ignore_case=True)

SERVER_SCRIPT = Path(__file__).parent / "server.py"

# TODO: Create a McpToolset instance for the MCP server
mcp_tools = None

local_tools = [get_weather]

def main():
    parser = argparse.ArgumentParser(description="Travel Assistant")
    parser.add_argument("prompt", type=str, nargs="?", help="User travel query prompt")
    args = parser.parse_args()

    if not args.prompt:
        user_prompt = prompt(HTML('<skyblue>Enter your travel query:</skyblue> '), completer=travel_completer)
    else:
        user_prompt = args.prompt

    print("\n=== Travel Assistant ===\n")    
    response = ask_agent(
        user_prompt,
        tools=[
            mcp_tools,
            *local_tools,
        ],
    )
    format_response(response)
    print("\n\n")

if __name__ == "__main__":
    main()
