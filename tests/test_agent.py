import asyncio
import os
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from travel_assistant.agent import root_agent
from google.genai import types as genai_types
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()  # load your .env

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment!")

client = Client(api_key=api_key)


async def main():
    """Runs the agent with a sample query."""
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="app", user_id="test_user", session_id="test_session"
    )
    runner = Runner(
        agent=root_agent, app_name="app", session_service=session_service
    )

    queries = [
        "Create a weekend getaway plan to Amsterdam from 15 to 17 Jan 2026, with local events, temperature, and travel tips.",
        "Can you suggest some popular tourist attractions in Amsterdam?",
        "looks good, I approve",
        "yes",
    ]

    for query in queries:
        print(f">>> {query}")
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=genai_types.Content(
                role="user", 
                parts=[genai_types.Part.from_text(text=query)]
            ),
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())