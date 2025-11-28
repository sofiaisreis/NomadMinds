from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.tools import FunctionTool

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# This is the function that the RefinerAgent will call to exit the loop.
def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the initial draft is finished and no more changes are needed."""
    return ({"status": "approved", "message": "Story approved. Exiting refinement loop."},)

print("✅ exit_loop function created.")

# This agent refines the story based on critique OR calls the exit_loop function.
events_refiner_agent = Agent(
    name="EventsRefinerAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction="""You are a story refiner. You have a proposal list of events and the respective critique about the choice of events.
    
    Story Draft: {events_proposal}
    Critique: {events_proposal_critique}
    
    Your task is to analyze the critique.
    - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the suggestions draft to fully incorporate the feedback from the critique.""",
    output_key="events_proposal",  # It overwrites the draft with the new, refined version.
    tools=[
        FunctionTool(exit_loop)
    ],  # The tool is now correctly initialized with the function reference.
)

print("✅ events_refiner_agent created.")
