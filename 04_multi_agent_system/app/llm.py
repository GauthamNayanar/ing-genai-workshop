"""Legacy direct-LLM helper kept for comparison with the multi-agent exercise.

The exercise app uses agent.py. Learners should edit agent.py and tools.py.
"""

import os

from google import genai
from google.genai.types import GenerateContentConfig


PROJECT_ID = ""  # Optional: replace with your project ID, or set GOOGLE_CLOUD_PROJECT.
LOCATION = "europe-west4"
MODEL_NAME = "gemini-2.5-flash"


def _client() -> genai.Client:
    """Create a Vertex AI client using ADC/WIF credentials, not API keys."""
    project_id = PROJECT_ID or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise RuntimeError(
            "Set PROJECT_ID in llm.py or export GOOGLE_CLOUD_PROJECT. "
            "This workshop uses Vertex AI with ADC/WIF credentials, not API keys."
        )

    return genai.Client(
        vertexai=True,
        project=project_id,
        location=LOCATION,
    )


# Set a default system message for the model
SYSTEM_MESSAGE = """
    You are a helpful travel assistant.
    You have access to tools. Decide whether you need to use a tool.
    - If needed, use it
    - Otherwise, answer directly
"""


def ask_llm(
    prompt: str,
    system_instruction: str = SYSTEM_MESSAGE,
    temperature: float = 0.7,
    top_k: int = 40,
    top_p: float = 1.0,
    tools: list = None,
    # Add more parameters as needed
) -> str:
    """Send a prompt to the LLM and return the text response."""
    config = GenerateContentConfig(
        system_instruction=system_instruction,  # <-- Sets the model's persona/behavior for all responses
        temperature=temperature,                # <-- Controls randomness: 0=deterministic, 1=creative, 2=very random
        top_p=top_p,                            # <-- Nucleus sampling: considers tokens with cumulative probability up to this value
        top_k=top_k,                            # <-- Limits sampling to the top K most likely tokens at each step
        tools=tools,                            # <-- Pass the list of tools the model can use (if any)
    )
    response = _client().models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )
    return response.text
