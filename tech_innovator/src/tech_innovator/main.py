from tech_innovator.crews.content_development.content_development_crew import ContentDevelopmentCrew
from tech_innovator.crews.Marketing_strategy.marketing_strategy_crew import MarketingStrategyCrew
from pydantic import BaseModel
from crewai.flow.flow import start, listen, Flow


from dotenv import load_dotenv

load_dotenv()  

class TechState(BaseModel):
    topic: str = ""

class TechInnovator(Flow[TechState]):

    @start()
    def Give_topic(self):
        self.state.topic = input("Enter the topic for the content development: ")

    @listen(Give_topic)
    def Content_development(self):
        result = ContentDevelopmentCrew().crew().kickoff(inputs={"topic": self.state.topic})
        print(result)
        return result

    @listen(Content_development)
    def Marketing_strategy(self, result):
        result = MarketingStrategyCrew().crew().kickoff(inputs={"output": result})
        print(result)
        return result

def main():
    tech_innovator = TechInnovator()
    result = tech_innovator.kickoff()
    print(result)





