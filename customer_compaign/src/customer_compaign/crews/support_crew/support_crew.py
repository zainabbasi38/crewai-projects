from crewai import Agent, Task, Crew , Process
from crewai.project import CrewBase, agent , crew, task
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool
from customer_compaign.tools.custom_tool import SentimentAnalysisTool

@CrewBase
class SupportCrew():

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    directory_read_tool = DirectoryReadTool(directory='./src/customer_compaign/crews/support_crew/instructions')
    file_read_tool = FileReadTool()
    search_tool = SerperDevTool()
    sentiment_analysis_tool = SentimentAnalysisTool()

    @agent
    def sales_rep_agent(self) -> Agent:
        return Agent(config= self.agents_config["sales_rep_agent"])
    
    @agent
    def lead_sales_rep_agent(self) -> Agent:
        return Agent(config= self.agents_config["lead_sales_rep_agent"])
    
    @task
    def lead_profiling_task(self) ->Task:
        return Task(
            config= self.tasks_config["lead_profiling_task"], tools = [self.directory_read_tool, self.file_read_tool, self.search_tool]
            )
    
    @task
    def personalized_outreach_task(self) ->Task:
        return Task(
            config= self.tasks_config["personalized_outreach_task"], tools = [self.sentiment_analysis_tool, self.search_tool]
            )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents= self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True
        )
