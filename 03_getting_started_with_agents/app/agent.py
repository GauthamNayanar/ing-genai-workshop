import asyncio
import uuid

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

PROJECT_ID = ""  # <-- Replace with your project ID
LOCATION = "europe-west4"
MODEL_NAME = "gemini-2.5-flash"

APP_NAME = "Travel-Assistant"
USER_ID = "workshop-user"

# Set a default system message for the model
SYSTEM_MESSAGE = """
    You are a helpful travel assistant.
    You have access to tools. Decide whether you need to use a tool.
    - If needed, use it
    - Otherwise, answer directly
"""


def ask_agent(
    prompt: str,
    tools: list | None = None,
) -> str:
    """Send a prompt to the agent and return the text response."""
    return asyncio.run(_ask_agent(prompt=prompt, tools=tools))


async def _ask_agent(
    prompt: str,
    tools: list | None = None,
) -> str:
    # TODO: Create an Agent
    agent = Agent(None)

    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    # TODO: Create the runner that will execute the agent
    runner = Runner(None)

    # TODO: Wrap the user prompt in a Content message
    message = types.Content(None)

    # TODO: Iterate through the agent events and return the final response
    async for event in runner.run_async(None):
        pass

    return ""
