from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from pydantic import BaseModel
from typing import List, Dict
import os
import logging
from app.utils.crew_logger import CrewLogger

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'product_pitch_crew.log')

logger = CrewLogger(
    log_file=log_file,
    log_level=logging.DEBUG,
    console_output=True
)

class ProductPitchesOutput(BaseModel):
    pitches: List[str]

@CrewBase
class ProductPitchCrew:
    """Generates persuasive pitches for each collaborative product."""

    @agent
    def marketing_writer(self) -> Agent:
        logger.logger.info("Creating product marketing writer agent")
        return Agent(
            role="Marketing Pitch Expert",
            goal="Write compelling and on-brand marketing pitches for collaborative products.",
            backstory="""You are a creative copywriter who brings product concepts to life through emotionally resonant language,
            always staying aligned with the core branding of both companies.""",
            tools=[],
            verbose=True
        )

    @task
    def generate_pitches(self) -> Task:
        logger.logger.info("Creating task to write product marketing pitches")
        return Task(
            description="""
            For each product in the input list, write a short, engaging pitch that:
            - Reflects the voice of both brands
            - Highlights the unique value of the collaboration
            - Includes a call to action

            Output a list of 5 pitch strings.
            """,
            expected_output="A list of 5 short product pitches.",
            output_pydantic=ProductPitchesOutput,
            agent=self.marketing_writer()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.marketing_writer()],
            tasks=[self.generate_pitches()],
            process=Process.sequential,
            verbose=True
        )

    async def kickoff(self, input_data: Dict) -> Dict:
        try:
            logger.logger.info(f"Kicking off ProductPitchCrew with input: {input_data}")
            crew_instance = self.crew()
            result = await crew_instance.kickoff_async(inputs=input_data)
            logger.logger.info(f"Pitch generation completed: {result}")
            return result
        except Exception as e:
            logger.logger.error(f"Error generating pitches: {str(e)}")
            raise
