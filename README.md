Manual runner: python run.py
ADK runner: adk run travel_assistant

ARCHITECTURE
============

Root Agent:
- Orchestrates the workflow using tools (wrapped subagents).

ParallelResearchTeam:
- Runs three subagents simultaneously:
    - events_pipeline_agent (Sequential: Research → Summarize)
    - weather_agent (OpenWeather API → current weather on a given city -> openstreetmap nominatim)
    - travel_tips_agent
- Each subagent writes its output to the shared session context.

AggregatorAgent:
- Runs after the parallel agents complete.
- Uses the outputs from all parallel subagents via {placeholder} syntax.
- Generates a single executive summary.

Context flow:
- Shared session context ensures outputs from parallel agents are available to the aggregator.
- This allows seamless communication even though agents are in different files.


CONCEPTS USED
=============

✅ Key exam points demonstrated by this workflow:
- Multi-agent system: ParallelAgent + SequentialAgent
- Tools: AgentTool wrapping subagents
- Sessions & Memory: shared context between agents
- Context engineering: placeholders {final_events_summary}, etc.
- LLM-powered agents: all subagents use Gemini models