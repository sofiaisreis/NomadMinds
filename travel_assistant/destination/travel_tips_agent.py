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

# Travel tips Agent: Its job is to use the google_search tool and present travel tips for a particular country or city.
travel_tips_agent = LlmAgent(
    name="TravelTipsAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction="""You are a specialized travel tips agent. Your only job is to use the
    google_search tool to find good travel tips for a given place/city
    and present the findings with links to the respective event page.""",
    tools=[google_search],
    output_key="travel_tips_findings",  # The result of this agent will be stored in the session state with this key.
)

print("✅ travel_tips_agent created.")