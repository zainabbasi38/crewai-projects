from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class PlanningCrew:
    """Automate event planning Crew"""

  
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()


    @agent
    def venue_coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config["venue_coordinator"],tools= [self.search_tool, self.scrape_tool],
        )
    
    @agent
    def logistics_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["logistics_manager"],tools= [self.search_tool, self.scrape_tool],
        )
    
    @agent
    def marketing_communications_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["marketing_communications_agent"],tools= [self.search_tool, self.scrape_tool],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def venue_task(self) -> Task:
        return Task(
            config=self.tasks_config["venue_task"],
        )
    
    @task
    def logistics_task(self) -> Task:
        return Task(
            config=self.tasks_config["logistics_task"],
        )
    
    @task
    def marketing_task(self) -> Task:
        return Task(
            config=self.tasks_config["marketing_task"],
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
