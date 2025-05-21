from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict
from crewai_tools import SerperDevTool
from pydantic import BaseModel
from app.utils.crew_logger import CrewLogger
import logging
import os

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'crew_execution.log')

logger = CrewLogger(
    log_file=log_file,
    log_level=logging.DEBUG,
    console_output=True
)

class CollaborationRecommendation(BaseModel):
    name: str
    industry: str
    rationale: str
    product_concept: str

class CollaborationOutput(BaseModel):
    input_summary: Dict[str, str]
    top_collaborating_brands: List[CollaborationRecommendation]
@CrewBase
class BrandCollabsCrew():
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.logger = logger

    @agent
    def collaboration_strategist(self) -> Agent:
        return Agent(
           role="Cross-Industry Collaboration Strategist",
            goal="Design imaginative, brand-driven partnerships using the given plastic material as a creative anchor.",
            backstory="""You are a top creative strategist at a global innovation agency. 
You specialize in designing iconic, cross-industry brand collaborations that blend sustainability, emotional resonance, and cultural relevance.

You think like a product visionary and marketer. You know how to turn recycled materials into symbols of innovation, nostalgia, or brand purpose.

You prioritize:
- Emotional storytelling
- Creative product concepts
- Unexpected brand pairings (e.g., tech + fashion, auto + toys)

Avoid boring or overly similar industry matches. Only use search if you need fresh brand ideas — not for research-heavy tasks.""",
            tools=[SerperDevTool()],
            verbose=False,
            allow_delegation=False
        )

    @task
    def identify_collaboration_opportunities(self) -> Task:
        return Task(
            description="""You are given two structured inputs: 'brand_data' and 'plastic_data'.

Your task is to recommend 5 creative **brand collaboration opportunities**.

Each recommendation must:
- Feature a **brand from a different industry** than the input brand.
- Include a **product concept** that meaningfully combines the brand identity, the collaborator’s identity, and the plastic material (symbolically or functionally).
- Include a **rationale** grounded in storytelling, emotional resonance, or shared brand ethos — not just shared sustainability focus.

Use the plastic material as a storytelling or innovation anchor (e.g., upcycled, symbolic, functional).

You may search **once** for inspiration (e.g., "iconic toy brands", "youth tech brands", or "eco-luxury fashion").

Avoid:
- Recommending brands in the same or very similar industry.
- Generic or obvious matches based purely on sustainability.

Think like a **brand innovation strategist** at a global agency developing high-visibility, cross-industry collabs.

Use this output format:

{
  "input_summary": {
    "brand": "Brief brand name and industry",
    "plastic": "Plastic type and one key property"
  },
  "top_collaborating_brands": [
    {
      "name": "string",
      "industry": "string",
      "rationale": "Why this brand is a creative and strategic match",
      "product_concept": "Surprising or emotionally resonant joint product idea using the plastic"
    }
  ]
}

Only return 5 brands. Less is okay if it improves creativity and quality.
""",
            agent=self.collaboration_strategist(),
            expected_output="""Use this exact format:

{
  "input_summary": {
    "brand": "Brief brand name and industry",
    "plastic": "Plastic type and one key property"
  },
  "top_collaborating_brands": [
    {
      "name": "string",
      "industry": "string",
      "rationale": "Why this brand is a good match",
      "product_concept": "Brief idea for a joint product"
    }
  ]
}

Return exactly 5 if confident, else fewer high-quality matches.
""",
            output_pydantic=CollaborationOutput
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False
        )

    async def kickoff(self, input_data: Dict) -> CollaborationOutput:
        try:
            if not isinstance(input_data, dict):
                raise ValueError("Input must be a dictionary")
            if "brand_data" not in input_data or "plastic_data" not in input_data:
                raise ValueError("Input must contain 'brand_data' and 'plastic_data'")
            logger.logger.info(f"Starting crew kickoff with input: {input_data}")
            crew_instance = self.crew()
            logger.logger.info("Crew instance created")
            result = await crew_instance.kickoff_async(inputs=input_data)
            logger.logger.info(f"Crew execution completed with result: {result}")
            # Ensure it's converted to a validated Pydantic object
            return result.to_dict()

        except Exception as e:
            logger.logger.error(f"Error in plastic analysis kickoff: {str(e)}")
            raise
