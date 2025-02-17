#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from customer_compaign.crews.support_crew.support_crew import SupportCrew
from dotenv import load_dotenv
load_dotenv()


class SupportState(BaseModel):
    lead_name: str =  "",
    industry: str = ""
    key_decision_maker:str =  ""
    position: str = ""
    milestone: str =  ""
    response : str = ""

class PoemFlow(Flow[SupportState]):

    @start()
    def info(self):
        print("getting information")
        self.state.lead_name = "DeepLearningAI"
        self.state.industry = "Online Learning Platform"
        self.state.key_decision_maker = "Andrew Ng"
        self.state.position = "CEO"
        self.state.milestone = "product Launch"

    @listen(info)
    def supporting_response(self):
        print("Generating response")
        result = (
            SupportCrew()
            .crew()
            .kickoff(inputs={"lead_name": self.state.lead_name, "industry": self.state.industry, "key_decision_maker": self.state.key_decision_maker, "position":self.state.position, "milestone": self.state.milestone})
        )

        print("response generated", result.raw)
        self.state.response = result.raw

    @listen(supporting_response)
    def save_response(self):
        print("Saving response")
        with open("response.txt", "w") as f:
            f.write(self.state.response)


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
