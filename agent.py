from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search, AgentTool, FunctionTool
from google.genai import types
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from .events.events_pipeline_agent import events_pipeline_agent
from .destination.destination_weather_agent import weather_agent
from .destination.travel_tips_agent import travel_tips_agent

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# The ParallelAgent runs all its sub-agents simultaneously.
parallel_travel_assistant_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[events_pipeline_agent, weather_agent, travel_tips_agent],
)
print("✅ parallel_travel_assistant_team created.")

# The AggregatorAgent runs *after* the parallel step to synthesize the results.
aggregator_agent = Agent(
    name="AggregatorAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    # It uses placeholders to inject the outputs from the parallel agents, which are now in the session state.
    instruction="""Combine these three research findings into a single executive summary:

    **Events:**
    {final_events_summary}
    
    **Weather:**
    {weather_findings}
    
    **Travel Tips:**
    {travel_tips_findings}
    
    Your summary should highlight common themes, surprising connections, and the most important key takeaways from all three reports. The final summary should be around 200 words.""",
    output_key="executive_summary",  # This will be the final output of the entire system.
)
print("✅ aggregator_agent created.")


# The Root Agent orchestrates the entire workflow.
root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="""You are a travel assistant coordinator. Your goal is to answer the user's query by orchestrating a workflow.
        1. First, you MUST call the AgentTool that starts the `parallel_travel_assistant_team` to gather information on events, weather, and travel tips.
        2. Next, you MUST call the AgentTool that runs the `aggregator_agent` to synthesize the gathered information into a concise executive summary.
        3. Finally, present the final summary clearly to the user as your response.""",
    tools=[AgentTool(parallel_travel_assistant_team), AgentTool(aggregator_agent)],
)

print("✅ Root Agent defined.")