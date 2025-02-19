from crewai.flow.flow import Flow, start, listen, router
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

class Inquiry(Flow):
    user_query = input("Enter your query: ")

    @start()
    def start(self):
        response = completion(
            model = "gemini/gemini-1.5-flash",
            messages = [{"role": "user", "content": "Classify this query into one of these categories: 'general_inquiry', 'technical_inquiry', 'billing_inquiry', or 'not_an_inquiry'. Query: " + self.user_query}]
        )
        output = response.choices[0].message.content
        return output
    
    @router(start)
    def route_inquiry(self, output):
        output = output.lower().strip()
        if "general_inquiry" in output:
            return "general_inquiry"
        elif "technical_inquiry" in output:
            return "technical_inquiry"
        elif "billing_inquiry" in output:
            return "billing_inquiry"
        else:
            return "not_an_inquiry"
    
    @listen("general_inquiry")
    def general_inquiry_response(self):
        print("general_inquiry")
        response = completion(
            model = "gemini/gemini-1.5-flash",
            messages = [{"role": "user", "content": f"This is a general inquiry about PTCL Flash Fiber. Please provide a helpful response: {self.user_query}"}]
        )
        output = response.choices[0].message.content
        return output

    @listen("technical_inquiry")
    def technical_inquiry_response(self):
        print("technical_inquiry")
        response = completion(
            model = "gemini/gemini-1.5-flash",
            messages = [{"role": "user", "content": f"This is a technical inquiry about PTCL Flash Fiber. Please provide technical assistance: {self.user_query}"}]
        )
        output = response.choices[0].message.content
        return output

    @listen("billing_inquiry")
    def billing_inquiry_response(self):
        print("billing_inquiry")
        response = completion(
            model = "gemini/gemini-1.5-flash",
            messages = [{"role": "user", "content": f"This is a billing inquiry about PTCL Flash Fiber. Please provide billing-related assistance: {self.user_query}"}]
        )
        output = response.choices[0].message.content
        return output
    
    @listen("not_an_inquiry")
    def not_an_inquiry_response(self):
        print("not_an_inquiry")  
        response = completion(
            model = "gemini/gemini-1.5-flash",
            messages = [{"role": "user", "content": f"The user has asked about something not related to PTCL Flash Fiber. Politely inform them to ask relevant questions about PTCL Flash Fiber services: {self.user_query}"}]
        )
        output = response.choices[0].message.content
        return output

def main():
    task = Inquiry()
    result = task.kickoff()
    print("\nResponse:", result)
main()
def plot():
    task = Inquiry()
    task.plot()

plot()      