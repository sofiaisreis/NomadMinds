from .agent import root_agent
from .events.events_researcher_agent import events_researcher_agent
from .events.summarizer_agent import summarizer_agent
from .events.events_pipeline_agent import events_pipeline_agent
from .destination.destination_weather_agent import weather_agent
from .destination.travel_tips_agent import travel_tips_agent

agents = {
    "root": root_agent
}
