# Events pipeline, with the goal to answer the user's query about events by orchestrating a workflow.
#    1. First, it calls the subagent `events_researcher_agent` to find relevant events on the topic provided by the user.
#    2. Next, after receiving the events findings, it calls the `summarizer_agent` tool to create a concise summary.
#    3. Finally, it present the final summary clearly to the user as a response.

from google.genai import types
from google.adk.agents import SequentialAgent
from .events_researcher_agent import events_researcher_agent
from .summarizer_agent import summarizer_agent

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)


# --- SequentialAgent ---
# This agent orchestrates the pipeline by running the sub_agents in order.
events_pipeline_agent = SequentialAgent(
    name="EventsPipelineAgent",
    # The agents will run in the order provided: event_researcher -> summarizer
    sub_agents=[events_researcher_agent, summarizer_agent]
)

print("✅ Events pipeline agent defined.")