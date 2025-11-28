# Events pipeline, with the goal to answer the user's query about events by orchestrating a workflow.
#    1. First, it calls the subagent `events_researcher_agent` to find relevant events on the topic provided by the user.
#    2. Next, after receiving the events findings, it calls the `summarizer_agent` tool to create a concise summary.
#    3. Finally, it present the final summary clearly to the user as a response.

from google.genai import types
from google.adk.agents import SequentialAgent, LoopAgent
from .research.events_researcher_agent import events_researcher_agent
from .research.summarizer_agent import summarizer_agent
from .reviewers.events_critique_agent import events_critique_agent
from .reviewers.events_refiner_agent import events_refiner_agent

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# The LoopAgent contains the agents that will run repeatedly: Critic -> Refiner.
events_refinement_loopAgent = LoopAgent(
    name="EventsRefinementLoop",
    sub_agents=[events_critique_agent, events_refiner_agent],
    max_iterations=2,  # Prevents infinite loops
)


# The events_pipeline_agent agent is a SequentialAgent that defines the overall workflow: Initial Write -> Summary -> Refinement Loop.
events_pipeline_agent = SequentialAgent(
    name="EventsPipelineAgent",
    sub_agents=[events_researcher_agent, summarizer_agent, events_refinement_loopAgent],
)