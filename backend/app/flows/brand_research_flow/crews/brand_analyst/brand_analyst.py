from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool

@CrewBase
class BrandAnalystCrew():
   
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def brand_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['brand_researcher'],
            tools=[SerperDevTool()],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def plastic_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['plastic_analyst'],
            tools=[SerperDevTool()],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def collaboration_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['collaboration_strategist'],
            tools=[SerperDevTool()],
            verbose=True,
            allow_delegation=False
        )

    @task
    def analyze_target_brand(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_target_brand'],
            agent=self.brand_researcher(),
            output_file='brand_analysis.json'
        )

    @task
    def analyze_plastic_material(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_plastic_material'],
            agent=self.plastic_analyst(),
            output_file='plastic_analysis.json'
        )

    @task
    def identify_collaboration_opportunities(self) -> Task:
        return Task(
            config=self.tasks_config['identify_collaboration_opportunities'],
            agent=self.collaboration_strategist(),
            output_file='collaboration_opportunities.json'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Brand analysis Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True
        )
