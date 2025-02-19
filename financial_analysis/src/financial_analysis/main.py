#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from financial_analysis.crews.poem_crew.poem_crew import FinancialCrew
from dotenv import load_dotenv

load_dotenv()

class FinanacialAnalysisState(BaseModel):
    stock_selection: str = ""
    initial_capital: str = ""
    risk_tolerance: str = ""
    trading_strategy_preference: str = ""
    news_impact_consideration: bool = True
    financial_analysis: str = ""


class FinancialAnalysisFlow(Flow[FinanacialAnalysisState]):

    @start()
    def generate_stock_selection(self):
        print("Generating stock selection")
        self.state.stock_selection = "AAPL"
        self.state.initial_capital = "100000"
        self.state.risk_tolerance = "Medium"
        self.state.trading_strategy_preference = "Day Trading"
        self.state.news_impact_consideration = True

    @listen(generate_stock_selection)
    def generate_financial_analysis(self):      
        print("Generating financial analysis")
        result = FinancialCrew().crew().kickoff(inputs={
                "stock_selection": self.state.stock_selection,
                "initial_capital": self.state.initial_capital,
                "risk_tolerance": self.state.risk_tolerance,
                "trading_strategy_preference": self.state.trading_strategy_preference,
                "news_impact_consideration": self.state.news_impact_consideration,
            }
        )
        print("Financial analysis generated", result.raw)
        self.state.financial_analysis = result.raw

    @listen(generate_financial_analysis)
    def save_financial_analysis(self):
        print("Saving financial analysis")
        with open("financial_analysis.md", "w") as f:
            f.write(self.state.financial_analysis)


def kickoff():
    financial_analysis_flow = FinancialAnalysisFlow()
    financial_analysis_flow.kickoff()


def plot():
    financial_analysis_flow = FinancialAnalysisFlow()
    financial_analysis_flow.plot()


if __name__ == "__main__":
    kickoff()
