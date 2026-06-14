import asyncio
import os
import uuid

from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from tools import estimate_daily_budget, get_weather, search_flights


PROJECT_ID = ""  # Optional: replace with your project ID, or set GOOGLE_CLOUD_PROJECT.
LOCATION = "europe-west4"
MODEL_NAME = "gemini-2.5-flash"

APP_NAME = "Travel-Multi-Agent-Assistant"
USER_ID = "workshop-user"
SHOW_AGENT_EVENTS = False


def _configure_vertex_ai_auth() -> None:
    """Configure ADK to use Vertex AI with ADC/WIF credentials."""
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"

    if PROJECT_ID:
        os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
    elif "GOOGLE_CLOUD_PROJECT" not in os.environ:
        raise RuntimeError(
            "Set PROJECT_ID in agent.py or export GOOGLE_CLOUD_PROJECT. "
            "This workshop uses Vertex AI with ADC/WIF credentials, not API keys."
        )

    if LOCATION:
        os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
    elif "GOOGLE_CLOUD_LOCATION" not in os.environ:
        os.environ["GOOGLE_CLOUD_LOCATION"] = "europe-west4"


# Exercise 1: start with a single coordinator agent.
coordinator_agent = Agent(
    name="travel_coordinator",
    model=MODEL_NAME,
    description="Routes travel questions and produces a clear final answer.",
    instruction="""
You are a travel coordinator.
Answer simple travel questions directly.
For weather, flight, or budget questions, use the tools available to you.
Do not invent weather, flight, or budget data.
""",
    tools=[get_weather],
)


def make_weather_agent() -> Agent:
    """Create a weather specialist.

    ADK workflow agents can have only one parent, so each workflow needs its
    own specialist instances.
    """
    return Agent(
        name="weather_specialist",
        model=MODEL_NAME,
        description="Checks destination weather and packing implications.",
        instruction="""
You are a weather specialist.
Use get_weather when the user asks about weather or packing.
Return concise weather facts and practical packing advice.
""",
        tools=[get_weather],
        output_key="weather_report",
    )


def make_flight_agent() -> Agent:
    """Create a flight specialist."""
    return Agent(
        name="flight_specialist",
        model=MODEL_NAME,
        description="Finds available mock flights for a route.",
        instruction="""
You are a flight specialist.
Use search_flights when the user asks about flights or routes.
Return available options and clearly say when no mock route is available.
""",
        tools=[
            # TODO Exercise 2: add search_flights here.
        ],
        output_key="flight_report",
    )


def make_budget_agent() -> Agent:
    """Create a budget specialist."""
    return Agent(
        name="budget_specialist",
        model=MODEL_NAME,
        description="Estimates a daily budget for a destination and travel style.",
        instruction="""
You are a budget specialist.
Use estimate_daily_budget when the user asks about costs or budgets.
Return assumptions and the estimated daily amount.
""",
        tools=[
            # TODO Exercise 2: add estimate_daily_budget here.
        ],
        output_key="budget_report",
    )


# Exercise 2: specialist agents.
# Run these individually by switching root_agent below.
weather_agent = make_weather_agent()
flight_agent = make_flight_agent()
budget_agent = make_budget_agent()


# Exercise 3: sequential workflow.
# The agents run in this order. Later agents can reference prior outputs
# through instruction placeholders such as {weather_report}.
sequential_travel_pipeline = SequentialAgent(
    name="sequential_travel_pipeline",
    description="Runs weather, flight, budget, then synthesis in a fixed order.",
    sub_agents=[
        make_weather_agent(),
        make_flight_agent(),
        make_budget_agent(),
        Agent(
            name="sequential_synthesizer",
            model=MODEL_NAME,
            description="Combines specialist outputs into one travel plan.",
            instruction="""
Create a final travel plan from these specialist notes.

Weather report:
{weather_report}

Flight report:
{flight_report}

Budget report:
{budget_report}

If a report is missing or says data is unavailable, state that clearly.
Do not invent missing data.
""",
        ),
    ],
)


# Exercise 4: parallel workflow.
# Weather, flight, and budget can be researched independently, then a final
# synthesizer combines the results.
parallel_research_stage = ParallelAgent(
    name="parallel_research_stage",
    description="Runs independent travel research agents in parallel.",
    sub_agents=[
        make_weather_agent(),
        make_flight_agent(),
        make_budget_agent(),
    ],
)

parallel_travel_pipeline = SequentialAgent(
    name="parallel_travel_pipeline",
    description="Runs parallel research first, then synthesizes the result.",
    sub_agents=[
        parallel_research_stage,
        Agent(
            name="parallel_synthesizer",
            model=MODEL_NAME,
            description="Combines parallel specialist outputs into one answer.",
            instruction="""
Create a final travel recommendation from the parallel research results.

Weather report:
{weather_report}

Flight report:
{flight_report}

Budget report:
{budget_report}

Call out conflicts, missing data, and assumptions.
""",
        ),
    ],
)


# Exercise switch:
# 1. Start with coordinator_agent.
# 2. Try weather_agent, flight_agent, and budget_agent individually.
# 3. Switch to sequential_travel_pipeline.
# 4. Switch to parallel_travel_pipeline.
root_agent = coordinator_agent


def ask_agent(
    prompt: str,
    agent=root_agent,
) -> str:
    """Send a prompt to an ADK agent or workflow and return the final response."""
    return asyncio.run(_ask_agent(prompt=prompt, agent=agent))


async def _ask_agent(
    prompt: str,
    agent=root_agent,
) -> str:
    _configure_vertex_ai_auth()

    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=agent,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    final_text = ""

    async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=message):
        if SHOW_AGENT_EVENTS:
            print(f"Event from: {event.author}")
            for call in event.get_function_calls():
                print(f"Tool call: {call.name}({dict(call.args or {})})")

        if event.is_final_response() and event.content and event.content.parts:
            text_parts = [part.text for part in event.content.parts if part.text]
            if text_parts:
                final_text = "\n".join(text_parts)

    return final_text
