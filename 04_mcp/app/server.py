import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, stdio_client
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Travel MCP Server")


def _to_text(result: object) -> str:
    content = getattr(result, "content", None)
    if not content:
        return str(result)

    return "".join(
        getattr(item, "text", str(item)) for item in content
    )


def _normalize_location(value: str) -> str:
    return value.strip().title()


# MCP session helpers
async def _with_session(server_script, fn):
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(server_script).resolve())],
    )

    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            return await fn(session)


async def start_mcp_session(server_script="server.py"):
    server_path = Path(server_script).resolve()

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )

    return stdio_client(server_params)


async def list_tools(server_script="server.py"):
    async def run(session):
        tools = await session.list_tools()
        return [
            {"name": t.name, "description": t.description}
            for t in tools.tools
        ]

    return await _with_session(server_script, run)


async def call_tool(name, args=None, server_script="server.py"):
    args = args or {}

    async def run(session):
        result = await session.call_tool(name, args)
        try:
            return json.loads(_to_text(result))
        except json.JSONDecodeError:
            return _to_text(result)

    return await _with_session(server_script, run)


# load mock data
def _load_mock_data() -> dict:
    """Load mock flights data from the workshop data folder."""
    base_dir = Path(__file__).resolve().parents[2]
    data_dir = base_dir / "05_mcp" / "app" / "data"

    flights_file = data_dir / "mock_flights.json"

    if flights_file.exists():
        with open(flights_file, "r", encoding="utf-8") as flights_handle:
            flight_data = json.load(flights_handle)

        return flight_data

    raise FileNotFoundError(
        f"Could not find mock data files in {data_dir}"
    )


FLIGHT_DATA = _load_mock_data()


@mcp.tool()
def get_server_info() -> dict:
    """Return basic information about this MCP server."""
    return {
        "name": "Travel MCP Server",
        "purpose": "Demo server exposing weather and flight search tools",
        "tools": ["get_weather", "search_flights"],
    }


@mcp.tool()
def search_flights(origin: str, destination: str) -> list:
    """Search mock flights between two cities."""
    normalized_origin = _normalize_location(origin)
    normalized_destination = _normalize_location(destination)
    route = f"{normalized_origin}-{normalized_destination}"

    return FLIGHT_DATA.get(route, [])


# def add_your_own_too()


if __name__ == "__main__":
    mcp.run(transport="stdio")