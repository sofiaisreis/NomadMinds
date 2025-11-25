from google.adk.agents import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search, AgentTool, FunctionTool
from google.genai import types
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
import requests

print("✅ ADK components imported successfully.")

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

def get_coordinates(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    response = requests.get(url, headers={"User-Agent": "WeatherApp"})
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        print("lat:", float(data["lat"]), ", lon:", float(data["lon"]), ", for city: ", city)
        return float(data["lat"]), float(data["lon"])
    else:
        return None, None

def get_weather(city):
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        return "Could not find coordinates for this city."

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['current_weather']['temperature']
        wind = data['current_weather']['windspeed']
        return f"The current temperature in {city} is {temp}°C with wind speed {wind} km/h."
    else:
        return "Could not fetch weather data."

weather_tool = FunctionTool(
    func=get_weather
)

# Weather Agent: Its job is to use the google_search tool and present weather findings.
weather_agent = LlmAgent(
    name="WeatherAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a specialized weather agent. Your only job is to use the
    google_search tool to find how the weather is going to be, on a given time, on the given place or city
    and present the weather findings with links to the respective event page.""",
    tools=[weather_tool],
    output_key="weather_findings",  # The result of this agent will be stored in the session state with this key.
)

print("✅ weather_agent created.")