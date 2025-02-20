#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from job_application.crews.job_application_crew.job_applicaion_crew import JobApplicationCrew


class JobApplicationState(BaseModel):
    job_posting_url: str =  ""
    github_url: str = ""
    personal_writeup: str = ""
    job_application: str = ""


class JobApplicationFlow(Flow[JobApplicationState]):

    @start()
    def job_application_flow(self):
        print("Generating job application")
        self.state.job_posting_url =  'https://jobs.lever.co/AIFund/6c82e23e-d954-4dd8-a734-c0c2c5ee00f1?lever-origin=applied&lever-source%5B%5D=AI+Fund'
        self.state.github_url = 'https://github.com/joaomdmoura'
        self.state.personal_writeup = """Noah is an accomplished Software
        Engineering Leader with 18 years of experience, specializing in
        managing remote and in-office teams, and expert in multiple
        programming languages and frameworks. He holds an MBA and a strong
        background in AI and data science. Noah has successfully led
        major tech initiatives and startups, proving his ability to drive
        innovation and growth in the tech industry. Ideal for leadership
        roles that require a strategic and innovative approach."""

    @listen(job_application_flow)
    def generate_job_application(self):
        print("Generating job application")
        result = (
            JobApplicationCrew()
            .crew()
            .kickoff(inputs={"job_posting_url": self.state.job_posting_url, "github_url": self.state.github_url, "personal_writeup": self.state.personal_writeup})
        )

        print("Job application generated", result.raw)
        self.state.job_application = result.raw

    @listen(generate_job_application)
    def save_job_application(self):
        print("Saving job application")
        with open("job_application.txt", "w") as f:
            f.write(self.state.job_application)


def kickoff():
    job_application_flow = JobApplicationFlow()
    job_application_flow.kickoff()


def plot():
    job_application_flow = JobApplicationFlow()
    job_application_flow.plot()


if __name__ == "__main__":
    kickoff()
