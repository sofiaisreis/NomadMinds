from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# Events Agent: Its job is to use the google_search tool and present findings.
# This agent runs ONCE at the beginning to create the first draft.
events_researcher_agent = LlmAgent(
    name="EventsResearcherAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction="""You are a specialized events agent. Your only job is to use the
    google_search tool to find 4-5 pieces of relevant events on the given place/city for each day the user is traveling.
    Make sure to include a variety of event types (e.g., cultural, outdoor, food festivals, music, art exhibitions, sports, etc.).
    After gathering the information, present the findings with links to the respective event page.""",
    tools=[google_search],
    output_key="events_findings",  # The result of this agent will be stored in the session state with this key.
)

print("✅ events_researcher_agent created.")