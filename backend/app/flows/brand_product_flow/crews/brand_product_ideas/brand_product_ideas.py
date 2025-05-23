from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List, Dict
import os
import logging
from app.utils.crew_logger import CrewLogger

# Logging setup
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'product_idea_crew.log')

logger = CrewLogger(
    log_file=log_file,
    log_level=logging.DEBUG,
    console_output=True
)

# Pydantic Output Models
class ProductIdea(BaseModel):
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description for creative teams")
    creative_brief: str = Field(..., description="Brief for the creative pitch crew")
    visual_description: str = Field(..., description="Description for the image generation crew")

class ProductIdeasOutput(BaseModel):
    input_summary: Dict[str, str] = Field(..., description="Summary of input brands and material")
    products: List[ProductIdea] = Field(..., description="List of collaborative product ideas")

@CrewBase
class BrandProductIdeasCrew:
    """Generates product ideas for brand collaboration with briefs for downstream crews."""
    
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.logger = logger

    @agent
    def product_conceptualizer(self) -> Agent:
        logger.logger.info("Creating product conceptualizer agent")
        return Agent(
            role="Brand Collaboration Product Strategist",
            goal="Generate viable collaborative product concepts and provide clear briefs for creative pitch and image generation teams.",
            backstory="""You are a strategic product developer who specializes in brand collaborations. 
            Your job is to identify realistic product opportunities that make sense for both brands and 
            then provide clear, actionable briefs for the creative teams who will pitch and visualize these concepts.
            
            You think practically about what products could actually be manufactured using the given materials 
            while staying true to both brand identities. You write concise, inspiring briefs that give 
            creative teams everything they need to develop compelling pitches and visuals.
            
            You focus on products that feel natural and exciting, not forced partnerships.""",
            tools=[SerperDevTool()],
            verbose=False,
            allow_delegation=False
        )

    @task
    def generate_product_concepts(self) -> Task:
        logger.logger.info("Creating task to generate product concepts with creative briefs")
        return Task(
            description="""
             Based on '{source_brand_data}', '{target_brand_data}', and '{plastic_data}', generate 5 collaborative product ideas.
For each product, provide:
- **Name**: Clear, brandable product name
- **Description**: Concise product overview (30-40 words)
- **Creative Brief**: What the pitch crew needs to know to sell this concept (key benefits, positioning, target market)
- **Visual Description**: Brand aesthetic guidance for image generation - focus on which brand's core product to reimagine, key design elements from both brands, materials, and color palette suggestions

Focus on products that:
- Take an iconic item from one brand and reimagine it with the other's aesthetic
- Use the plastic material meaningfully in the design
- Could realistically be manufactured
- Represent clear brand DNA fusion

For visual descriptions, think about:
- Which brand contributes the base product form
- Which brand contributes the design aesthetic/technology
- How the plastic material influences the look and feel
- Suggested color palette that blends both brand identities

Output format:

{
  "input_summary": {
    "brand_1": "First brand name and core identity",
    "brand_2": "Second brand name and core identity", 
    "plastic_material": "Plastic type and key manufacturing properties"
  },
  "products": [
    {
      "name": "string",
      "description": "string",
      "creative_brief": "string",
      "visual_description": "string"
    }
  ]
}

Generate exactly 5 products that represent the best collaboration opportunities.""",
            agent=self.product_conceptualizer(),
            expected_output="""Return a JSON object with this structure:

{
  "input_summary": {
    "brand_1": "string",
    "brand_2": "string", 
    "plastic_material": "string"
  },
  "products": [
    {
      "name": "string",
      "description": "string (30-40 words)",
      "creative_brief": "string (pitch-focused)",
      "visual_description": "string (brand aesthetic guidance)"
    }
  ]
}

Provide exactly 5 well-considered product concepts with clear downstream briefs.""",
            output_pydantic=ProductIdeasOutput
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
        agents=[self.product_conceptualizer()],
        tasks=[self.generate_product_concepts()],
        process=Process.sequential,
        verbose=True
        )

    async def kickoff(self, input_data: Dict) -> Dict:
        try:
            logger.logger.info(f"Kicking off BrandProductIdeasCrew with input: {input_data}")
            if not isinstance(input_data, dict):
                raise ValueError("Input must be a dictionary with brand_data, target_brand, plastic_data.")
            crew_instance = self.crew()
            result = await crew_instance.kickoff_async(inputs=input_data)
            logger.logger.info(f"Product ideas generation completed: {result}")
            return result.to_dict()
        except Exception as e:
            logger.logger.error(f"Error generating product ideas: {str(e)}")
            raise
