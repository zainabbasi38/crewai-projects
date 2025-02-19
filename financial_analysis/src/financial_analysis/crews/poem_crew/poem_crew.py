from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class FinancialCrew:
    """Finanacial Analysis Crew"""

   
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    
    @agent
    def data_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["data_analyst_agent"],
            tools=[self.search_tool, self.scrape_tool],
        )
    
    @agent
    def trading_strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["trading_strategy_agent"],tools=[self.search_tool, self.scrape_tool],
        )
    
    @agent
    def execution_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["execution_agent"],tools=[self.search_tool, self.scrape_tool],
        )
    
    @agent
    def risk_management_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["risk_management_agent"],tools=[self.search_tool, self.scrape_tool],
        )


    @task
    def data_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_analysis_task"],
        )
    
    @task
    def strategy_development_task(self) -> Task:
        return Task(
            config=self.tasks_config["strategy_development_task"],
        )
    
    @task
    def execution_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["execution_planning_task"],
        )
    
    @task
    def risk_assessment_task(self) -> Task:
        return Task(
            config=self.tasks_config["risk_assessment_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
