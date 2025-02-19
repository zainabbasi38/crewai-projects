#!/usr/bin/env python

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from automate_event_planning.crews.poem_crew.poem_crew import PlanningCrew
from dotenv import load_dotenv
import os
# os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
# os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
load_dotenv()

class PlanningState(BaseModel):
    event_topic: str = ""
    event_description: str = ""
    event_city: str = ""
    tentative_date: str = ""
    expected_participants: int = 0
    budget: int = 0
    venue_type: str = ""
    response : str = ""


class PlanningFlow(Flow[PlanningState]):

    @start()
    def event_planning(self):
        print("Getting event planning inputs")
        self.state.event_topic =  "Tech Innovation Conference"
        self.state.event_description = "A gathering of tech innovators and industry leaders to explore future technologies."
        self.state.event_city = "San Francisco"
        self.state.tentative_date = "2024-09-15"
        self.state.expected_participants = 500
        self.state.budget = 20000
        self.state.venue_type = "Conference Hall"

    @listen(event_planning)
    def generate_event_planning(self):
        print("Generating event planning")
        result = (
            PlanningCrew()
            .crew()
            .kickoff(inputs={"event_topic": self.state.event_topic,
                            "event_description": self.state.event_description,
                            "event_city": self.state.event_city,
                            "tentative_date": self.state.tentative_date,
                            "expected_participants": self.state.expected_participants,
                            "budget": self.state.budget,
                            "venue_type": self.state.venue_type})
        )

        print("Event planning generated", result.raw)
        self.state.response = result.raw

    @listen(generate_event_planning)
    def save_event_planning(self):
        print("Saving event planning")
        with open("event_planning.txt", "w") as f:
            f.write(self.state.response)


def kickoff():
    planning_flow = PlanningFlow()
    planning_flow.kickoff()


def plot():
    planning_flow = PlanningFlow()
    planning_flow.plot()


if __name__ == "__main__":
    kickoff()
