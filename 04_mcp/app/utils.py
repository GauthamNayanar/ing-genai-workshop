import json
from typing import Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


console = Console()


def format_response(response: str):
    print("\n")
    console.print(Panel.fit("Travel Assistant", style="bold cyan"))

    # Render full markdown properly
    console.print(Markdown(response))


def pretty_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))

