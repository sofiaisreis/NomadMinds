from .agent import root_agent
from .events.research.events_researcher_agent import events_researcher_agent
from .events.research.summarizer_agent import summarizer_agent
from .events.reviewers.events_critique_agent import events_critique_agent
from .events.reviewers.events_refiner_agent import events_refiner_agent
from .events.events_pipeline_agent import events_pipeline_agent
from .destination.destination_weather_agent import weather_agent
from .destination.travel_tips_agent import travel_tips_agent
from .trends.trends_agent import trends_agent

agents = {
    "root": root_agent
}
