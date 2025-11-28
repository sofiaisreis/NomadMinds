PROJECT OVERVIEW - NOMADMINDS
=============================
<img width="1536" height="1024" alt="NomadMinds" src="https://github.com/user-attachments/assets/97d663bd-8a66-4744-916f-86a532c92f7b" />

This project consists in an extensible AI travel advisor using parallel research agents, iterative critique loops, and contextual aggregation to produce high-quality travel recommendations. 
The agent is built using Google Agent Development Kit (ADK) and follows a modular architecture.

STARTUP
=======
- Get your google API key [here](https://aistudio.google.com/api-keys)
- Add .env file with:
```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=<your-google-api-key>
```

- Activate a python environment, and install adk:
```
python3 -m venv .venv &&
source .venv/bin/activate &&
pip install google-adk &&
pip install "httpx<0.28" &&
pip install mcp-server-fetch
```

TO RUN:
- ADK runner: ```adk run travel_assistant```
- To run in local: ```adk web --port 8000```
- To run with debug messages: ```adk web --log_level DEBUG```

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

Loop agent (travel_advisor_agent and travel_critique_agent):
- The travel advisor calls the parallel agent
- Then, the critique agent evaluates the ouput of the aggregator agent
- If the content is good, it follows to the next step, otherwise we repeat the parallel flow

Context engineer and Session:
- Created a stateful agent using InMemorySessionService
Shared session context ensures outputs from parallel agents are available to the aggregator.

Logs:
- Logs are enabled
- To activate, run: adk  web --log_level DEBUG

Using MCP:
- Used MCP server to Fetch (Web scrapping)
- https://github.com/modelcontextprotocol/servers?tab=readme-ov-file#%EF%B8%8F-official-integrations 

CONCEPTS USED
=============
- Multi-agent system: ParallelAgents + SequentialAgents + LoopAgents
- Tools: AgentTool wrapping subagents
- Sessions: shared context between agents
- Context engineering: placeholders {final_events_summary}, etc.
- LLM-powered agents: all subagents use Gemini models
- Logging system

======================
Example queries to run:
- Tell me what to do in lisbon from 27th november to 30 november 2025
- What are the top 5 photo spots trending in Rome today?

PROJECT STRUCTURE
=====================
The project is organized as follows:
 - travel_assistant/: The main Python package for the agent.
     - agent.py: Defines the root_agent and the sub-agents orchestration
     - events/: Contains the sub-agents responsible to gather the events summary
         - events/research: reserchers of events
            - events_researcher_agent.py: Using google search, finds pieces of relevant events on the given place/city for each day the user is traveling.
            - summarizer_agent.py: Uses the outputkey from the researcher and creates a concise summary as a bulleted list.
         - events/reviewers: reviewers of events
            - events_critique_agent.py: A constructive travelling advisor critic that reviews the events suggestions proposal and marks it at APPROVED or not.
            - events_refiner_agent.py: A refiner that takes the proposal list of events and the respective critique about the choice of events, providing updated where needed.
         - events_pipeline_agent.py: Responsible to launch the pipeline of event gathering, summarization and to call the loop refiner agent.
     - destination/: Contains the sub-agents responsible to gather the weather and travel tips
        - destination_weather_agent.py: Uses the weather_tool (which fecthes from open APIs) to find how the weather on a given time, in a city.
    - trends/: Finds the trends for the city
        - trends_agent.py: Agent using Official MCP server to Fetch (Web Scraping)