from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from tools.tools import search_tool, industry_match_tool, image_generator_tool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class ProductIdeaGeneratorCrew():
    """PlasticReuseCrew orchestrates agents for plastic upcycling analysis."""

    @agent
    def creative_pitch_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_pitch_generator'],
            tools=[search_tool],
            verbose=True,
            allow_delegation=True
        )
    @task
    def generate_creative_pitches_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_creative_pitches_task'],
            agent=self.creative_pitch_generator(),
            output_file='plastic_reuse_analysis.json',  
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the creative product ideas Crew"""
       
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True
        )
