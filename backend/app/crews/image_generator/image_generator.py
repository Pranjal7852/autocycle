from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from tools.tools import search_tool, industry_match_tool, image_generator_tool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class ImageGeneratorCrew():
   
    @agent
    def image_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['image_generator'],
            tools=[image_generator_tool],
            verbose=True,
            allow_delegation=False,
            max_iterations=5
        )

    @task
    def generate_image_task(self) -> Task:
        """Generates an image from a product pitch and integrates with the creative pitch task."""
        return Task(
            config=self.tasks_config['generate_image_task'],
            agent=self.image_generator(),
            output_file='generated_image.json',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Image generation Crew"""
       
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True
        )
