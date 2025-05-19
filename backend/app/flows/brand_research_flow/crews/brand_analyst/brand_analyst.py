from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict
from crewai_tools import SerperDevTool
from app.utils.crew_logger import CrewLogger
from pydantic import BaseModel
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

# Consistent structured output model for brand analysis
class BrandProfile(BaseModel):
    name: str
    industry: str
    main_products: List[str]
    sustainability_initiatives: List[str]
    plastic_materials_used: List[str]
    past_collaborations: List[str]
    operational_regions: List[str]

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
                role="Sustainability Brand Researcher",
                goal="Identify a brand's plastic use, sustainability initiatives, and regional operations with minimal queries",
                backstory="""You are an expert in brand sustainability analysis, capable of extracting valuable insights
                from a single comprehensive search. Your research helps identify potential collaboration opportunities
                between brands based on material usage and geographic reach.""",
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
                Research the brand '{brand}' using ONLY ONE smart search query:
                Example: "{brand} sustainability initiatives plastic usage collaborations manufacturing regions"

                Extract from the first result only:
                1. Brand industry and core product categories
                2. Any plastic materials the brand uses or recycles
                3. Any past or current sustainability collaborations
                4. Their operational or manufacturing regions
                
                If 'location' is given, prefer sources relevant to that region.
                
                DO NOT perform more than one query. DO NOT infer data.
                """,
                agent=self.brand_researcher(),
                expected_output="A JSON string representing a BrandProfile with the brand's industry, products, sustainability initiatives, plastic materials, collaborations, and regions.",
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
