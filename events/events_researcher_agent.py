from google.adk.agents import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search, AgentTool, FunctionTool
from google.genai import types
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# Events Agent: Its job is to use the google_search tool and present findings.
events_researcher_agent = LlmAgent(
    name="EventsResearcherAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a specialized events agent. Your only job is to use the
    google_search tool to find 3-4 pieces of relevant events on the given place/city
    and present the findings with links to the respective event page.""",
    tools=[google_search],
    output_key="events_findings",  # The result of this agent will be stored in the session state with this key.
)

print("✅ events_researcher_agent created.")