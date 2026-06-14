# utils.py
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()


def format_response(response: str):
    print("\n")
    console.print(Panel.fit("ADK Travel Assistant", style="bold cyan"))

    # Render full markdown properly
    console.print(Markdown(response))
