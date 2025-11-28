PROJECT OVERVIEW - NOMADMINDS
=============================
This project consists in an extensible AI travel advisor using parallel research agents, iterative critique loops, and contextual aggregation to produce high-quality travel recommendations. 
The agent is built using Google Agent Development Kit (ADK) and follows a modular architecture.

<img width="1536" height="1024" alt="NomadMinds" src="https://github.com/user-attachments/assets/97d663bd-8a66-4744-916f-86a532c92f7b" />


PROBLEM STATEMENT
=================
Planning a trip typically requires gathering and synthesizing information from many different sources: events happening in the area, weather forecasts, safety considerations, cultural norms, transportation details, and personalized travel tips. Each of these tasks requires different types of data and reasoning, and doing them manually is time-consuming, repetitive, and prone to incomplete results.

As travel becomes more spontaneous and dynamic, travelers need intelligent systems that can quickly research, filter, and summarize diverse information streams into actionable recommendations. The problem is interesting because it involves real-time data, multimodal reasoning, and coordination across multiple subtasks: an area where traditional single-prompt LLM tools are limited.

My project attempts to build a travel assistant that can fully automate this workflow using a coordinated AI multi-agent system.


SOLUTION STATEMENT
==================
To address the complexity of modern travel planning, we designed a coordinated multi-agent system that automates the full travel-research workflow. A single model prompt cannot efficiently manage the diverse subtasks involved—such as event discovery, weather forecasting, semantic retrieval of travel insights, and quality control—because each requires different tools, data sources, and reasoning styles.

Our solution uses specialized agents, each equipped with its own instructions and tools, working together under the orchestration of a Root Agent.
This architecture provides: parallelization, tool integration, iterative refinement, and shared context, which together create a modular, extensible, and robust system ideally suited for capturing and synthesizing the heterogeneous data sources required in travel planning.

The resulting architecture—illustrated in the project diagram—centers on a Root Agent that coordinates a mix of parallel, sequential, and looping subprocesses. This design allows the system to automatically gather real-time event information, check weather conditions, surface personalized travel advice, ensure output quality, and assemble everything into cohesive recommendations.


INSTALATION & CONFIGURATION
===========================
This project was built against Python 3.11.3.
It is suggested you create a vitrual environment using your preferred tooling e.g. uv.
Install dependenies -> check [requirements.txt](/requirements.txt)


TO RUN
======
- From the command line of the working directory execute the following command: ```adk run travel_assistant```
- Running the Agent in ADK Web mode: ```adk web --port 8000```
- To run with debug messages: ```adk web --log_level DEBUG```
- To run the integration test:```python -m tests.test_agent```


CONCEPTS USED
=============
- Multi-agent system: ParallelAgents + SequentialAgents + LoopAgents
- Tools: AgentTool and wrapping subagents
- MCP server: Fetch (Web scraping)
- Sessions: stateful agent using InMemorySessionService
- Context engineering: placeholders {final_events_summary}, etc.
- LLM-powered agents: all subagents use Gemini models
- Logging system (To activate, run: adk  web --log_level DEBUG)
- Integration tests

PROJECT STRUCTURE
=====================
The project is organized as follows:
 - **travel_assistant/**: The main Python package for the agent.
     - agent.py: Defines the root_agent and the sub-agents orchestration
     - **events/**: Contains the sub-agents responsible to gather the events summary
         - **events/research**: reserchers of events
            - events_researcher_agent.py: Using google search, finds pieces of relevant events on the given place/city for each day the user is traveling.
            - summarizer_agent.py: Uses the outputkey from the researcher and creates a concise summary as a bulleted list.
         - **events/reviewers**: reviewers of events
            - events_critique_agent.py: A constructive travelling advisor critic that reviews the events suggestions proposal and marks it at APPROVED or not.
            - events_refiner_agent.py: A refiner that takes the proposal list of events and the respective critique about the choice of events, providing updated where needed.
         - events_pipeline_agent.py: Responsible to launch the pipeline of event gathering, summarization and to call the loop refiner agent.
     - **destination/**: Contains the sub-agents responsible to gather the weather and travel tips
        - destination_weather_agent.py: Uses the weather_tool (which fecthes from open APIs) to find how the weather on a given time, in a city.
    - **trends/**: Finds the trends for the city
        - trends_agent.py: Agent using Official MCP server to Fetch (Web Scraping)
 - **tests/**: Contains integration tests for the agent.


WORKFLOW
============
**root_agent:**
- Orchestrates the workflow using tools to call a sequential agent (that provides all information on events, weather and tips summarized), and an agent that delivers trends.

**parallel_travel_assistant_team:**
- Runs three subagents simultaneously:
    - events_pipeline_agent (Sequential: Research → Summarize -> Loop agent)
        - The Loop agent iterates through events_critique_agent and events_refiner_agent and if the content is good, it follows to the next step, otherwise we repeat the loop.
    - weather_agent (OpenWeather API → current weather on a given city -> openstreetmap nominatim)
    - travel_tips_agent
- Each subagent writes its output to the shared session context.

**aggregator_agent:**
- Runs after the parallel_travel_assistant_team completes.
- Uses the outputs from all parallel subagents via {placeholder} syntax.
- Generates a single executive summary.

**trends_agent:**
- Accesses the MCP server to gather trends, when user requests.

[Check the workflow's schema here.](/workflowschema.png)


Example queries to run:
======================
- Tell me what to do in lisbon from 27th november to 30 november 2025
- What are the top 5 photo spots trending in Rome today?
- What’s the 7-day weather forecast for Tokyo, and any major events happening there?
- Suggest a 3-day food & culture itinerary for Barcelona for a vegan traveler.
- List upcoming outdoor concerts in Berlin over the next two weeks.
- Create a weekend getaway plan to Amsterdam from 15 to 17 Jan 2026, with local events and budget-friendly transport.
