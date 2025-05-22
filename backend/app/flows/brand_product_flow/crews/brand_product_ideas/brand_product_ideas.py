from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool
from pydantic import BaseModel
from typing import List, Dict
import os
import logging
from app.utils.crew_logger import CrewLogger

# Logging setup
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'product_idea_crew.log')

logger = CrewLogger(
    log_file=log_file,
    log_level=logging.DEBUG,
    console_output=True
)

# Pydantic Output
class ProductIdea(BaseModel):
    name: str
    description: str

class ProductIdeasOutput(BaseModel):
    products: List[ProductIdea]

@CrewBase
class BrandProductIdeasCrew:
    """Generates innovative product ideas combining two brands and a plastic material."""

    @agent
    def idea_generator(self) -> Agent:
        logger.logger.info("Creating product idea generator agent")
        return Agent(
            role="Creative Brand Collaborator",
            goal="Invent 5 innovative, eco-friendly products that combine the essence of both brands using the specified plastic material.",
            backstory="""You're a trend-setting product designer who thrives at the intersection of brand identity and sustainability.
            Your expertise is in conceptualizing fan-favorite products that feel authentic to both companies.""",
            tools=[SerperDevTool()],
            verbose=True,
            allow_delegation=False
        )

    @task
    def generate_ideas(self) -> Task:
        logger.logger.info("Creating task to generate collaborative product ideas")
        return Task(
            description="""
            Based on the source brand data, target brand name, and plastic type, invent 5 collaborative product ideas.

            For each product, include:
            - Name
            - Short description (max 50 words)

            These products should blend elements of both brands and creatively integrate the use of the given plastic material.
            Format your final answer as a list of JSON objects.
            """,
            expected_output="A JSON list of 5 products with 'name' and 'description'.",
            output_pydantic=ProductIdeasOutput,
            agent=self.idea_generator()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.idea_generator()],
            tasks=[self.generate_ideas()],
            process=Process.sequential,
            verbose=True
        )

    async def kickoff(self, input_data: Dict) -> Dict:
        try:
            logger.logger.info(f"Kicking off BrandProductIdeasCrew with input: {input_data}")
            if not isinstance(input_data, dict):
                raise ValueError("Input must be a dictionary with brand_data, target_brand, plastic_data.")
            crew_instance = self.crew()
            result = await crew_instance.kickoff_async(inputs=input_data)
            logger.logger.info(f"Product ideas generation completed: {result}")
            return result
        except Exception as e:
            logger.logger.error(f"Error generating product ideas: {str(e)}")
            raise
