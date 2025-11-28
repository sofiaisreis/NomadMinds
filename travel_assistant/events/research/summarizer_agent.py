from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# Summarizer Agent: Its job is to summarize the text it receives.
summarizer_agent = LlmAgent(
    name="SummarizerAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    # The instruction is modified to request a bulleted list for a clear output format.
    instruction="""Read the provided research findings: {events_findings}
Create a concise summary as a bulleted list with 3-5 key points about each event.""",
    output_key="events_proposal",  # The result of this agent will be stored in the session state with this key.
)

print("✅ summarizer_agent created.")