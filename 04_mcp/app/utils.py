# utils.py
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()


def format_response(response: str):
    print("\n")
    console.print(Panel.fit("LLM Travel Assistant", style="bold cyan"))

    # Render full markdown properly
    console.print(Markdown(response))


import json
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def pretty_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))

