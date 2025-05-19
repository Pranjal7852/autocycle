from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict
from crewai_tools import SerperDevTool
from app.utils.crew_logger import CrewLogger
import time

logger = CrewLogger(log_file="crew_execution.log", console_output=True)

@CrewBase
class BrandCollabsCrew():
   
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.logger = logger
        

    @agent
    def collaboration_strategist(self) -> Agent:
        return Agent(
            role="Sustainable Collaboration Innovator",
            goal="Based on comprehensive analyses of a target brand '{brand}' and a specific plastic '{plastic_type}', identify and list 5 distinct brand names that are prime candidates for strategic collaboration to develop innovative products using the upcycled plastic. Provide supporting rationale for each.",
            backstory="""You are a visionary strategist at the intersection of brand marketing, sustainable product development, and circular economy principles.
            With a keen eye for market trends and consumer desire for eco-conscious products, you excel at forging unlikely yet powerful partnerships.
            You can see the "big picture," connecting a brand's image and values with the tangible potential of a specific upcycled material to pinpoint
            ideal collaboration partners. Your network and understanding of diverse industries allow you to identify and select the most promising brands for impactful co-creation.""",
            tools=[SerperDevTool()],
            verbose=False,
            allow_delegation=False
        )

    @task
    def identify_collaboration_opportunities(self) -> Task:
        return Task(
            description="""Based on brand '{brand}' and plastic '{plastic_type}' profiles, identify 5 high-fit brand partners for collaboration. 
            Use brand synergy, sustainability alignment, and upcycling creativity as criteria.
            
            Expected output format:
            {
                "summary": {
                    "brand": "...",
                    "plastic": "..."
                },
                "top_5_collaborating_brand_names": [...],
                "collaboration_proposals": [
                    {
                        "brand": "...",
                        "rationale": "...",
                        "product_idea": "...",
                        "synergy_score": 8.5
                    }
                ]
            }""",
            agent=self.collaboration_strategist(),
            output_file='collaboration_opportunities.json'
        )

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
        """Run the brand collaboration crew"""
        try:
            crew_instance = self.crew()
            result = await crew_instance.kickoff_async(inputs=input)
            return result
        except Exception as e:
            self.logger.error(f"Error in brand collaboration: {str(e)}")
            raise
        