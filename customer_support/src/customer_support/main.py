from customer_support.crews.poem_crew.poem_crew import CustomerSupportCrew
from crewai.flow.flow import Flow, start , listen
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

class SupportState(BaseModel):
    customer : str = ""
    person : str = ""
    inquiry : str = ""
    support_response : str = ""

class CustomerSupport(Flow[SupportState]):
    
    @start()
    def customer_info(self):
        self.state.customer= "DeepLearningAI"
        self.state.person = "Andrew Ng"
        self.state.inquiry = "I need help with setting up a Crew and kicking it off, specifically how can I add memory to my crew? Can you provide guidance?"

    @listen(customer_info)
    def customer_support_flow(self):
        response = CustomerSupportCrew().crew().kickoff(inputs = {

            "customer": self.state.customer,
            "person": self.state.person,
            "inquiry": self.state.inquiry
        })
        print(f"Customer Support Response: {response.raw}")
        self.state.support_response = response.raw
        return response
    
    

    @listen(customer_support_flow)
    def answer(self):
        print("Tkank you for response")
        with open("customer_support_response.txt", "w") as f:
            f.write(self.state.support_response)

def kickoff():
    flow = CustomerSupport()
    flow.kickoff()

def plot():
    flow = CustomerSupport()
    flow.plot()