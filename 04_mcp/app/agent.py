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

    agent = Agent(
        name="Travel Assistant",
        model=MODEL_NAME,
        instruction=SYSTEM_MESSAGE,
        tools=tools or [],
    )

    # Set up session management for the agent
    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    # Create a runner to execute the agent
    runner = Runner(
        app_name=APP_NAME,
        agent=agent,
        session_service=session_service,
    )

    # Format the user prompt as a message
    message = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    # Run the agent
    async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=message):
        if event.is_final_response() and event.content and event.content.parts:
            return "\n".join(
                part.text
                for part in event.content.parts
                if part.text
            )

    return ""