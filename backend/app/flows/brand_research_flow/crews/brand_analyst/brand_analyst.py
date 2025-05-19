from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict
from crewai_tools import SerperDevTool
from app.utils.crew_logger import CrewLogger
import yaml
import os
import logging

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'crew_execution.log')

logger = CrewLogger(
    log_file=log_file,
    log_level=logging.DEBUG,  # Set to DEBUG for more detailed logging
    console_output=True
)

@CrewBase
class BrandAnalystCrew():
    """Brand Analysis crew"""
    
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.logger = logger
        self.config_dir = os.path.join(os.path.dirname(__file__), 'config')
        try:
            self.agents_config = self._load_yaml_config('agents.yaml')
            self.tasks_config = self._load_yaml_config('tasks.yaml')
            self.logger.logger.info("Successfully loaded configuration files")
        except Exception as e:
            self.logger.logger.error(f"Error loading configuration files: {str(e)}")
            raise

    def _load_yaml_config(self, filename: str) -> dict:
        config_path = os.path.join(self.config_dir, filename)
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                if not config:
                    raise ValueError(f"Empty configuration in {filename}")
                self.logger.logger.debug(f"Loaded config from {filename}: {config}")
                return config
        except Exception as e:
            self.logger.logger.error(f"Error loading {filename}: {str(e)}")
            raise

    @agent
    def brand_researcher(self) -> Agent:
        try:
            agent_config = self.agents_config['brand_researcher']
            self.logger.logger.info("Creating brand researcher agent with config")
            return Agent(
                config=agent_config,  # type: ignore[index]
                verbose=True,
                tools=[SerperDevTool()]
            )
        except Exception as e:
            self.logger.logger.error(f"Error creating brand researcher agent: {str(e)}")
            raise

    @task
    def analyze_target_brant(self) -> Task:
        try:
            task_config = self.tasks_config['analyze_target_brand']
            self.logger.logger.info("Creating analyze target brand task with config")
            return Task(
                config=task_config  # type: ignore[index]
            )
        except Exception as e:
            self.logger.logger.error(f"Error creating analyze target brand task: {str(e)}")
            raise

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

    async def kickoff(self, input: Dict) -> Dict:
        """Run the brand analysis crew"""
        try:
            self.logger.logger.info(f"Starting crew kickoff with input: {input}")
            crew_instance = self.crew()
            self.logger.logger.info("Crew instance created")
            result = await crew_instance.kickoff_async(inputs=input)
            self.logger.logger.info(f"Crew execution completed with result: {result}")
            return result
        except Exception as e:
            self.logger.logger.error(f"Error in brand analysis: {str(e)}")
            raise
        