from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict
from crewai_tools import SerperDevTool
from app.utils.crew_logger import CrewLogger
import time

logger = CrewLogger(log_file="crew_execution.log", console_output=True)

@CrewBase
class PlasticAnalystCrew():
   
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.logger = logger
        

    @agent
    def plastic_analyst(self) -> Agent:
        return Agent(
            role="Plastic Materials Analyst",
            goal="Analyze and provide detailed information about plastic materials, their properties, and environmental impact",
            backstory="""You are an expert in plastic materials analysis with extensive knowledge of polymer science, 
            material properties, and environmental impact assessment. You have years of experience in analyzing 
            different types of plastics and their applications.""",
            tools=[SerperDevTool()],
            verbose=False,
            allow_delegation=False
        )
    
    @task
    def analyze_plastic_material(self) -> Task:
        return Task(
            description="""Analyze the given plastic material and provide detailed information about:
            1. Material composition and properties
            2. Environmental impact and sustainability
            3. Common applications and use cases
            4. Recycling potential and methods
            5. Alternatives and recommendations""",
            agent=self.plastic_analyst(),
            output_file='plastic_analysis.json',
            expected_output="""A detailed analysis of the plastic material in JSON format containing:
            {
                "material_composition": {
                    "name": "string",
                    "chemical_structure": "string",
                    "properties": ["string"]
                },
                "environmental_impact": {
                    "sustainability_score": "number",
                    "degradation_time": "string",
                    "environmental_concerns": ["string"]
                },
                "applications": ["string"],
                "recycling": {
                    "potential": "string",
                    "methods": ["string"],
                    "challenges": ["string"]
                },
                "alternatives": [
                    {
                        "name": "string",
                        "description": "string",
                        "sustainability_advantage": "string"
                    }
                ]
            }"""
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Plastic analysis Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True
        )
    
    async def kickoff(self, input: Dict) -> Dict:
        """Run the brand collaboration crew"""
        try:
            crew_instance = self.crew()
            result = await crew_instance.kickoff_async(inputs=input)
            return result
        except Exception as e:
            self.logger.logger.error(f"Error in Plastic Analyst: {str(e)}")
            raise
            
        