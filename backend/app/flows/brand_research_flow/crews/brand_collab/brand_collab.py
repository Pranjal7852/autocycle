from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from app.utils.crew_logger import CrewLogger
from typing import List, Dict, Optional
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
    brand_name: str = Field(description="Name of the collaborating brand")
    brand_placement: List[str] = Field(description="Key brand positioning attributes")
    sustainability_placement: str = Field(description="Brand's sustainability approach")
    product_assumptions: List[str] = Field(description="Potential physical product types")
    collaboration_summary: str = Field(description="Brief description of the collaboration concept")
    estimated_impact: Optional[int] = Field(default=None, description="Potential environmental or market impact in million")
    confidence_score: Optional[int] = Field(default=None, description="Confidence score")
    combined_reach: Optional[int] = Field(default=None, description="Combined marketing reach of both brands in millions")

class CollaborationOutput(BaseModel):
    input_summary: Dict[str, str] = Field(description="Summary of input brand and plastic data")
    top_collaborations: List[CollaborationRecommendation] = Field(description="List of collaboration recommendations")

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
            goal="Design physical product collaborations using sustainable plastic materials as the creative and functional core.",
          backstory="""You are an expert strategic product designer with deep expertise in circular economy innovation
and cross-industry partnerships. You specialize in creating compelling physical product collaborations that combine
brand storytelling with sustainable material innovation.

Your core competencies include:
- Identifying synergistic brand partnerships across different industries
- Leveraging recycled and renewable plastic properties for functional design
- Creating products that enhance both brands' market positioning
- Ensuring manufacturability and market viability of collaboration concepts
- Understanding consumer psychology and sustainable product adoption

You think like an industrial designer who deeply understands brand equity, material science, and market dynamics.
Your recommendations are always grounded in physical, manufacturable products that tell a compelling sustainability story.""",
            tools=[SerperDevTool()],
            verbose=False,
            allow_delegation=False
        )
    
    @agent  
    def market_analyst(self) -> Agent:
        return Agent(
            role="Sustainable Product Market Analyst",
            goal="Validate collaboration concepts for market viability and consumer appeal.",
            backstory="""You are a market research specialist focused on sustainable product launches and brand collaborations.
You analyze market trends, consumer behavior, and competitive landscapes to ensure collaboration recommendations
have strong commercial potential.

You evaluate:
- Market readiness for sustainable product innovations
- Consumer willingness to pay for collaborative products
- Competitive positioning and differentiation opportunities
- Regulatory and supply chain considerations
- Brand alignment and potential market conflicts""",
            tools=[SerperDevTool()],
            verbose=False,
            allow_delegation=False
        )

    @task
    def identify_collaboration_opportunities(self) -> Task:
        return Task(
            description="""Analyze the provided brand data '{brand_data}' and plastic material data '{plastic_data}' 
to generate up to 5 innovative cross-industry physical product collaboration recommendations.

For each recommendation, provide:
- brand_name: The collaborating brand name
- brand_placement: List of 2-3 key positioning attributes (e.g., ["Premium quality", "Scandinavian design", "Sustainability leader"])
- sustainability_placement: Their current sustainability positioning or commitment
- product_assumptions: List of 2-4 specific physical product concepts that could work (e.g., ["Chair", "Toy", "Shoe"])
- collaboration_summary: 2-3 sentence description explaining the collaboration concept and its strategic value
- estimated_impact: Estimated potential environmental or market impact in millions (revenue, carbon savings, etc.)
- confidence_score: Your confidence in this recommendation on a scale of 1-100
- combined_reach: Combined marketing reach of both brands in millions (social media followers, customers, newsletter subscribers, etc.)

Focus exclusively on physical, manufacturable products. Consider:
- How the plastic material's properties enable unique product features
- How the collaboration enhances both brands' market positioning
- Realistic manufacturing and distribution considerations
- Consumer appeal and willingness to purchase

Prioritize collaborations that create genuine value for both brands and demonstrate clear sustainability benefits.""",
            agent=self.collaboration_strategist(),
            expected_output="""Return your output using this format exactly:

{
  "input_summary": {
    "brand": "string",
    "plastic": "string"
  },
  "top_collaborations": [
    {
      "brand_name": "string",
      "brand_placement": ["string", ...],
      "sustainability_placement": "string",
      "product_assumptions": ["string", ...],
      "collaboration_summary": "string"
      "estimated_impact": "int"
    "confidence_score": "int"
    "combined_reach":t "int"
    }
  ]
}

Return up to 5 ideas max. Only include physical products that make sense given the brands and plastic properties.
"""
,
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
