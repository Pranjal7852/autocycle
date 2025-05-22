from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from pydantic import BaseModel
from typing import List, Dict
import os
import logging
from app.utils.crew_logger import CrewLogger

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'product_image_crew.log')

logger = CrewLogger(
    log_file=log_file,
    log_level=logging.DEBUG,
    console_output=True
)

class ProductImagesOutput(BaseModel):
    images: List[str]  # Can be prompts or image URLs

@CrewBase
class ProductImageCrew:
    """Generates image prompts or AI visuals for each collaborative product."""

    @agent
    def concept_visualizer(self) -> Agent:
        logger.logger.info("Creating concept visualizer agent")
        return Agent(
            role="Concept Artist",
            goal="Generate visual prompts that represent collaborative product designs.",
            backstory="""You are a visionary product illustrator using AI to bring ideas to life through vivid, accurate visual prompts.""",
            tools=[],
            verbose=True
        )

    @task
    def generate_images(self) -> Task:
        logger.logger.info("Creating image generation task")
        return Task(
            description="""
            For each product, generate a vivid and detailed prompt suitable for use with an AI image generation tool like DALL·E.

            Each prompt should reflect the product's style, branding elements, and use of the provided plastic material.

            Output a list of 5 prompts or links (if image generation is integrated).
            """,
            expected_output="A list of 5 image prompts.",
            output_pydantic=ProductImagesOutput,
            agent=self.concept_visualizer()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.concept_visualizer()],
            tasks=[self.generate_images()],
            process=Process.sequential,
            verbose=True
        )

    async def kickoff(self, input_data: Dict) -> Dict:
        try:
            logger.logger.info(f"Kicking off ProductImageCrew with input: {input_data}")
            crew_instance = self.crew()
            result = await crew_instance.kickoff_async(inputs=input_data)
            logger.logger.info(f"Image generation completed: {result}")
            return result
        except Exception as e:
            logger.logger.error(f"Error generating images: {str(e)}")
            raise
