from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool, MDXSearchTool


@CrewBase
class JobApplicationCrew:
    """Job Application Crew"""


    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    search_tool = SerperDevTool()   
    scrape_tool = ScrapeWebsiteTool()
    # read_resume = FileReadTool(file_path='./fake_resume.md')
    # semantic_search_resume = MDXSearchTool(mdx='./fake_resume.md')


    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[self.search_tool, self.scrape_tool],
        )

    @agent
    def profiler(self) -> Agent:
        return Agent(
            config=self.agents_config["profiler"],
            tools=[self.search_tool, self.scrape_tool],
        )

    @agent
    def resume_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_strategist"],
            tools=[self.search_tool, self.scrape_tool],
        )

    @agent
    def interview_preparer(self) -> Agent:
        return Agent(
            config=self.agents_config["interview_preparer"],
            tools=[self.search_tool, self.scrape_tool],
        )       

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def profile_task(self) -> Task:
        return Task(
            config=self.tasks_config["profile_task"],
        )

    @task
    def resume_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_strategy_task"],
        )

    @task
    def interview_preparation_task(self) -> Task:
        return Task(
            config=self.tasks_config["interview_preparation_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Job Application Crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
