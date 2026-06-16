# ing-genai-workshop

Practical exercises for the GenAI Workshop run by ING Analytics


## Setup

1. Configure Google authentication and project access from One Day Sandbox

```bash
bash scripts/setup_gcloud.sh <PROJECT_ID>
```

2. Create and activate the Python environment:

```bash
bash scripts/setup_venv.sh
source .venv/bin/activate
```

3. Make sure the virtual environment is active before running any app or notebook.

## Exercises

- `01_getting_started_with_llm/` — basic direct LLM usage with `google.genai`.
  - Teaches prompt construction, system instructions, and a simple `ask_llm()` wrapper.

- `03_getting_started_with_agents/` — ADK agent with tool usage.
  - Shows how to build an agent and pass tools.

- `04_mcp/` — ADK + MCP server integration.
  - Demonstrates exposing reusable tools through an MCP server and discovering/using tools from an agent.

## Notes

- `scripts/setup_gcloud.sh` configures `gcloud`, logs in with the workshop WIF login config, and enables the AI Platform API.
The workshop uses Application Default Credentials/Vertex AI rather than API keys.
- `scripts/setup_venv.sh` creates a `.venv` virtual environment and installs requirements from `requirements.txt`.