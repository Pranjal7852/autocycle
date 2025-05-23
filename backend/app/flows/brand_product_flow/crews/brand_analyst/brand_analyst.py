from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict
from crewai_tools import SerperDevTool
from app.utils.crew_logger import CrewLogger
from app.models.schemas import BrandProfile
import os
import logging

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'crew_execution.log')

logger = CrewLogger(
    log_file=log_file,
    log_level=logging.DEBUG,
    console_output=True
)

@CrewBase
class BrandAnalystCrew:
    """Crew for analyzing brand details and sustainability collaborations."""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def brand_researcher(self) -> Agent:
        try:
            logger.logger.info("Creating Sustainability Brand Researcher agent")
            return Agent(
               role="Brand Similarity Research Expert",
                goal="Extract clean, structured data that represents a brand's identity, material usage, and sustainability philosophy for vector matching.",
                backstory="""You specialize in researching and summarizing brand identities for semantic comparison. Your research helps match brands with similar products, values, materials, and markets.""",
                tools=[SerperDevTool()],
                verbose=True,
                allow_delegation=False
            )
        except Exception as e:
            logger.logger.error(f"Error creating Brand Researcher agent: {str(e)}")
            raise

    @task
    def analyze_target_brand(self) -> Task:
        try:
            logger.logger.info("Creating analyze_target_brand task")
            return Task(
                description="""
               Using only one intelligent web search (e.g., "{brand} sustainability philosophy plastic materials manufacturing regions"),
extract and return the following fields in JSON:

{
  "brand": "{brand}",
  "industry": "e.g., automotive, sportswear",
  "product_categories": ["e.g., sneakers", "sportswear"],
  "plastic_materials": ["e.g., PET", "EVA foam", "TPU"],
  "sustainability_philosophy": "e.g., circular economy, carbon-neutral by 2030, zero waste",
  "key_partners_or_collaborators": ["e.g., Parley for the Oceans", "UNEP"],
  "manufacturing_regions": ["e.g., Europe", "Southeast Asia"],
  "brand_positioning": "e.g., luxury performance, eco-friendly mass market"
}

Only extract confirmed information from a reliable source like the brand's site or a news article.
Prefer sources relevant to '{location}' if provided.
                """,
                agent=self.brand_researcher(),
                expected_output="A clean JSON string compatible with the BrandProfile schema for vector embedding.",
                output_pydantic=BrandProfile
            )
        except Exception as e:
            logger.logger.error(f"Error creating analyze_target_brand task: {str(e)}")
            raise

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
        )

    async def kickoff(self, input_data: Dict) -> Dict:
        try:
            if not isinstance(input_data, dict):
                raise ValueError("Input must be a dictionary")
            if "brand" not in input_data:
                raise ValueError("Input dictionary must contain a 'brand' key")
            if not isinstance(input_data["brand"], str) or not input_data["brand"].strip():
                raise ValueError("'brand' must be a non-empty string")

            logger.logger.info(f"Starting BrandAnalystCrew with input: {input_data}")
            crew_instance = self.crew()
            logger.logger.info("Crew instance created")
            result = await crew_instance.kickoff_async(inputs=input_data)
            logger.logger.info(f"Crew execution completed with result: {result}")
            return result
        except ValueError as ve:
            logger.logger.error(f"Input validation error: {str(ve)}")
            raise
        except Exception as e:
            logger.logger.error(f"Error in brand analysis: {str(e)}")
            raise
