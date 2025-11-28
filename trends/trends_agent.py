"""
Trending Agent using Official MCP server to Fetch (Web Scraping).
https://github.com/modelcontextprotocol/servers/tree/main/src/fetch
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.tools import FunctionTool
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

# Setup Official Fetch MCP Server
mcp_fetch_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command= "python",
            args=[
                "-m",
                "mcp_server_fetch",
                ],
            #tool_filter=["fetch"],
        ),
        timeout=30,
    )
)

print("✅ MCP Fetch Server configured")

# Trends Agent
trends_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    name="TrendsAgent",
    instruction="""You are a trend analysis agent.
        When given a location:
        1. Use the MCP `fetch` tool to retrieve HTML from Google Search or Trend sources.
        2. Parse the returned HTML and extract trending topics.
        3. Summarize 5–10 CURRENT and RECENT trends.
        4. Categorize each trend (tech, food, entertainment, politics, sports, etc.)
        5. Explain WHY each is trending.""",
    tools=[mcp_fetch_server],
)

print("✅ Trends Agent created successfully!\n")
