from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from google.genai import types
from google.adk.agents import Agent
from .destination.destination_weather_agent import weather_agent
from .destination.travel_tips_agent import travel_tips_agent
from .events.events_pipeline_agent import events_pipeline_agent
from .trends.trends_agent import trends_agent
from google.adk.sessions.in_memory_session_service import InMemorySessionService
import logging
import os

print("✅ ADK components imported successfully.")

APP_NAME = "default"  # Application
USER_ID = "default"  # User
SESSION = "default"  # Session

# Clean up any previous logs
for log_file in ["logger.log", "web.log", "tunnel.log"]:
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🧹 Cleaned up {log_file}")

# Configure logging with DEBUG log level.
logging.basicConfig(
    filename="logger.log",
    level=logging.ERROR,
    format="%(filename)s:%(lineno)s %(levelname)s:%(message)s",
)

print("✅ Logging configured")
retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# Set up Session Management
# InMemorySessionService stores conversations in RAM (temporary)
session_service = InMemorySessionService()

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
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    # It uses placeholders to inject the outputs from the parallel agents, which are now in the session state.
    instruction="""Combine these three research findings into a single executive summary:

    **Events:**
    {events_proposal}
    
    **Weather:**
    {weather_findings}
    
    **Travel Tips:**
    {travel_tips_findings}
    
    Your summary should highlight common themes, surprising connections, and the most important key takeaways from all three reports. The final summary should be around 200 words.""",
    output_key="executive_summary",  # This will be the final output of the entire system.
)
print("✅ aggregator_agent created.")

# The sequ_runs_agent agent is a SequentialAgent that defines the overall workflow: ParallelAgent -> Aggregator.
sequ_runs_agent = SequentialAgent(
    name="SequentiallyRunsAgents",
    sub_agents=[parallel_travel_assistant_team, aggregator_agent],
)

# The Root Agent orchestrates the entire workflow.
root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="""You are a travel assistant coordinator. Your goal is to answer the user's query by orchestrating a workflow.
        1. First, call the trends_agent to get the current trends in a specified location if needed, and present it to the user. 
        2. Then MUST call the seq_runs_agent that will ultimately give you information on events, weather, and travel tips, which is happening in a certain location at a certain time.
        3. Finally, present the final summary clearly to the user as your response. Use emojis to highlight important aspects. Even funny ones!
        4. Don't forget to be engaging and enthusiastic in your final output! Use bullet points where appropriate.""",
    tools=[AgentTool(trends_agent),AgentTool(sequ_runs_agent)],
)
print("✅ Root Agent defined.")
print("✅ Stateful agent initialized!")
print(f"   - Application: {APP_NAME}")
print(f"   - User: {USER_ID}")
print(f"   - Using: {session_service.__class__.__name__}")