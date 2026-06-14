#mTravel Assistant App


## What this app combines

- [x] v1: basic Travel Assistant
- [x] v2: better prompt shape and supplied context
- [x] v3: Google ADK tool-using assistant with routing
- [ ] v4: MCP-inspired tool registry with `list_tools()` and `call_tool(...)`

## Exercise

- Complete the ADK agent implementation in `agent.py`.

#### Notes:
- `llm.py` is included as a comparison path: it uses `google.genai` and `genai.client` to make a direct `client.models.generate_content(...)` call.
- `agent.py` is the preferred approach in this folder because ADK is designed for tool-enabled agent workflows, with structured agent definitions, tool integration, and session-based execution.
