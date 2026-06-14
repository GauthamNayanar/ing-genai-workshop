# ADK Multi-Agent Travel Assistant Exercise

In this exercise you will build a travel assistant from multiple specialist
agents. You will compare:

- a single coordinator agent
- individual specialist agents
- a sequential workflow
- a parallel workflow

The app is intentionally incomplete. Your job is to wire tools into specialist
agents, switch the active `root_agent`, and compare behavior.

## Files to edit

- `agent.py`: defines specialist agents and multi-agent workflows
- `tools.py`: contains mock tools used by the specialists

You usually do not need to edit:

- `app.py`: command-line wrapper
- `utils.py`: response formatting
- `llm.py`: legacy direct-LLM comparison helper

## Authentication

This app uses Google ADK with Vertex AI and Application Default Credentials.
It does not use API keys.

Before running it, authenticate with the workshop WIF flow and make sure a
project is available either by setting `PROJECT_ID` in `agent.py` or exporting:

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="europe-west4"
```

## Run the app

From this folder:

```bash
python app.py "I am planning a weekend work trip from Amsterdam to Lisbon. What should I pack, is there a flight, and what budget should I expect?"
```

From the repository root:

```bash
python 04_multi_agent_system/app/app.py "I am planning a weekend work trip from Amsterdam to Lisbon. What should I pack, is there a flight, and what budget should I expect?"
```

## Exercise 1: Start with a coordinator

Open `agent.py` and find:

```python
root_agent = coordinator_agent
```

The starter coordinator has only the weather tool.

Run:

```bash
python app.py "I am visiting Lisbon this weekend. What should I pack?"
```

Expected result:

- The coordinator should answer using `get_weather`
- It should not be able to answer flight or budget questions yet

## Exercise 2: Wire specialist agents

Open `agent.py`.

Find:

- `weather_agent`
- `flight_agent`
- `budget_agent`

The weather specialist is already wired. Complete the other two:

```python
flight_agent = Agent(
    ...
    tools=[search_flights],
)

budget_agent = Agent(
    ...
    tools=[estimate_daily_budget],
)
```

Test each specialist by temporarily switching:

```python
root_agent = flight_agent
```

Then:

```python
root_agent = budget_agent
```

Run prompts that only require that specialist.

Examples:

```bash
python app.py "Is there a flight from Amsterdam to Lisbon?"
python app.py "What is a student daily budget for Lisbon?"
```

## Exercise 3: Build a sequential workflow

A sequential workflow runs agents in a fixed order.

In `agent.py`, inspect `sequential_travel_pipeline`:

```python
SequentialAgent(
    sub_agents=[
        weather_agent,
        flight_agent,
        budget_agent,
        sequential_synthesizer,
    ],
)
```

Switch:

```python
root_agent = sequential_travel_pipeline
```

Run:

```bash
python app.py "I am planning a weekend work trip from Amsterdam to Lisbon. What should I pack, is there a flight, and what budget should I expect?"
```

Expected result:

- Weather runs first
- Flight runs second
- Budget runs third
- The synthesizer combines `{weather_report}`, `{flight_report}`, and `{budget_report}`

Questions:

- What happens if the user only asks about weather?
- Does the sequential workflow still run every specialist?
- When is that useful, and when is it wasteful?

## Exercise 4: Build a parallel workflow

A parallel workflow runs independent agents at the same time.

In `agent.py`, inspect:

```python
parallel_research_stage = ParallelAgent(...)
parallel_travel_pipeline = SequentialAgent(...)
```

Switch:

```python
root_agent = parallel_travel_pipeline
```

Run the same broad travel prompt.

Expected result:

- Weather, flight, and budget research can run independently
- A final synthesizer combines their outputs

Compare with sequential:

- Which design is easier to reason about?
- Which design should be faster for independent research?
- Which design is better when one step depends on a previous step?

## Exercise 5: Debug agent events

Open `agent.py` and set:

```python
SHOW_AGENT_EVENTS = True
```

Run the sequential and parallel workflows again.

Observe:

- Which agent produced each event
- Which tools were called
- Whether parallel and sequential workflows emit events differently

## Exercise 6: Add a conflict-checking agent

Open `tools.py` and complete `check_trip_conflicts`.

Then create a new specialist in `agent.py`:

```python
conflict_agent = Agent(
    name="conflict_checker",
    model=MODEL_NAME,
    instruction="Find risks, conflicts, and missing data in the reports.",
    tools=[check_trip_conflicts],
    output_key="conflict_report",
)
```

Add it after the research stage and before final synthesis.

Challenge:

- In a sequential workflow, make it run after all research agents
- In a parallel workflow, make it run after `parallel_research_stage`
- Update the synthesizer to include `{conflict_report}`

## Exercise 7: Choose the right architecture

For each task, decide whether single-agent, sequential, or parallel is best:

- "What should I pack for Lisbon?"
- "Plan a work trip with weather, flights, budget, and policy checks."
- "First validate the request, then search for flights only if required info exists."
- "Compare weather, flights, and budget independently, then summarize."

Write down your reasoning.

## Capstone

Build a multi-agent travel planner that:

- Validates the request
- Runs independent research in parallel where possible
- Runs dependent checks sequentially
- Produces a final answer with sections:
  - Weather
  - Flights
  - Budget
  - Risks or missing data
  - Recommendation

The goal is not just to make it answer. The goal is to justify why each agent is
sequential or parallel.
