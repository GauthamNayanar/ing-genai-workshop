from google import genai
from google.genai.types import GenerateContentConfig


PROJECT_ID = ""  # <-- Replace with your project ID
LOCATION = "europe-west4"
MODEL_NAME = "gemini-2.5-flash"


client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)


# Set a default system message for the model
SYSTEM_MESSAGE = """
    You are a travel guide for Amsterdam. 
    Based on the visitor's preferences, suggest 3 specific activities.
    Keep responses concise with bullet points.
"""

# TODO: Define the ask_llm function to call the Gemini and return the response text
def ask_llm(
    prompt: str,
    system_instruction: str = SYSTEM_MESSAGE,
    temperature: float = 0.7,
    top_k: int = 40,
    top_p: float = 1.0,
) -> str:
    """Send a prompt to the LLM and return the text response."""
    return None
