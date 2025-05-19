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

class PlasticMaterialProfile(BaseModel):
    type: str
    properties: List[str]
    applications: List[str]
    environmental_impact: str
    recycling_potential: str
    regional_relevance: str = ""

@CrewBase
class PlasticAnalystCrew:
    """Crew for analyzing plastic materials and their properties."""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def plastic_analyst(self) -> Agent:
        try:
            logger.logger.info("Creating Plastic analyst agent")
            return Agent(
                role="Plastic Materials Analyst",
                goal="Provide a summarized, structured understanding of any plastic type in one shot",
                backstory=(
                    "You are a polymer expert helping a sustainability initiative. You must answer clearly and briefly "
                    "with insights from a single well-formed search. Focus on structure, recycling, and applications."
                ),
                tools=[SerperDevTool()],
                verbose=True,
                allow_delegation=False
            )
        except Exception as e:
            logger.logger.error(f"Error creating plastic analyst agent: {str(e)}")
            raise

    @task
    def analyze_plastic_material(self) -> Task:
        try:
            logger.logger.info("Creating analyze plastic material task")
            return Task(
                description=(
                    "Search for '{plastic_type}' properties, common uses, recycling info, and environmental impact.\n"
                    "Use just ONE search query such as: '{plastic_type} polymer structure usage recycling sustainability'\n\n"
                    "Extract and summarize ONLY from this single search:\n"
                    "1. Key properties and material composition\n"
                    "2. Most common industrial or consumer uses\n"
                    "3. Recyclability and methods\n"
                    "4. Environmental concerns (e.g., biodegradability, pollution potential)\n"
                    "5. Region-specific info if '{location}' is provided\n"
                ),
                agent=self.plastic_analyst(),
                expected_output=(
                "A JSON object containing the plastic type, key properties, common applications, "
                "environmental impact, recycling potential, and region-specific information (if provided)."
            ),
            output_pydantic=PlasticMaterialProfile
            )
        except Exception as e:
            logger.logger.error(f"Error creating analyze plastic task: {str(e)}")
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
            if "plastic_type" not in input_data:
                raise ValueError("Input must include 'plastic_type'")
            if not input_data["plastic_type"]:
                raise ValueError("'plastic_type' must be a non-empty string")

            logger.logger.info(f"Starting crew kickoff with input: {input_data}")
            crew_instance = self.crew()
            logger.logger.info("Crew instance created")
            result = await crew_instance.kickoff_async(inputs=input_data)
            logger.logger.info(f"Crew execution completed with result: {result}")
            return result
        except Exception as e:
            logger.logger.error(f"Error in plastic analysis kickoff: {str(e)}")
            raise