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

# Critique Agent: Its job is to evaluate the result of the aggregator agent.
events_critique_agent = LlmAgent(
    name="TravelCritiqueAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction="""You are a constructive travelling advisor critic. Review the events suggestions provided below.
    Output: {events_proposal}
    Evaluate the suggestion's veracity, likeability, and reason to your best knowledge.
    - If the draft with the suggestions is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
    output_key="events_proposal_critique",  # Stores the feedback in the state.
)

print("✅ summarizer_agent created.")