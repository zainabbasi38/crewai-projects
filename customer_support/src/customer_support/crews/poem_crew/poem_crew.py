from crewai import Agent, Task, Crew,Process
from crewai.project import crew, agent, task, CrewBase
from crewai_tools import ScrapeWebsiteTool

@CrewBase
class CustomerSupportCrew():

    docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
    )

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def support_agent(self) -> Agent:
        return Agent(config = self.agents_config["support_agent"],)

    @agent
    def support_quality_assurance_agent(self) -> Agent:
        return Agent(config = self.agents_config["support_quality_assurance_agent"],)

    @task
    def inquiry_resolution(self) -> Task:
        return Task(config= self.tasks_config["inquiry_resolution"],tools=[self.docs_scrape_tool])

    @task
    def quality_assurance_review(self) -> Task:
        return Task(config= self.tasks_config["quality_assurance_review"],)

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""

        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True
        )