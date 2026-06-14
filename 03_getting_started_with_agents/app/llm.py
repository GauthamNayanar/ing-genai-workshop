from google import genai
from google.genai.types import GenerateContentConfig


PROJECT_ID = ""  # <-- Replace with your project ID
LOCATION = "europe-west4"
MODEL_NAME = "gemini-2.5-flash"


client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)


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
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )
    return response.text