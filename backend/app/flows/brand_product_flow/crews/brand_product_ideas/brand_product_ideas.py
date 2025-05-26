from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
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
    product_type: str = Field(..., description="Type or category of the product")
    name: str = Field(..., description="Product name (2-3 words)")
    description: str = Field(..., description="Product description (30-40 words)")

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
    role="AI-Driven Brand Synergy Strategist",
    goal="Identify compelling, manufacturable product ideas for cross-brand collaborations and translate them into detailed, visual-friendly prompts for AI content generation teams.",
    backstory="""You are a hybrid strategist and creative technologist specializing in brand collaborations. 
    Your mission is to spot realistic and visually striking opportunities where two brands can meet—whether 
    through form, function, material use, or shared values.

    You prioritize products that can be realistically prototyped or produced, ensuring they align with 
    both brands' manufacturing strengths and aesthetic codes. You excel in translating abstract brand traits 
    into concrete product visions that feel innovative yet natural.

    Your deliverables include succinct briefs and AI-ready image prompts written for generative models.
    These briefs guide visual creators with exact product type suggestions, form factor hints, 
    material cues, and color palettes rooted in commercial aesthetics.

    You avoid cliché mashups and instead look for clever, grounded intersections between the two brands. 
    Every idea should feel like a premium concept ready for the pitch room or the next design sprint.""",
    
    verbose=True,
    allow_delegation=True
)

    @task
    def generate_product_concepts(self) -> Task:
        logger.logger.info("Creating task to generate product concepts with creative briefs")
        return Task(
            description="""
You are generating **strategic and visually-inspiring product concepts** for a collaboration between two brands, centered around a sustainable plastic material.

---

🔎 **Context:**
- **Source Brand**: `{source_brand_data}`
  - This brand contributes its **signature plastic material** and associated identity (e.g., color, texture, sustainability ethos).
- **Target Brand**: `{target_brand_data}`
  - This brand provides the **product category** and **consumer-facing platform** for the final item.
- **Plastic Material Data**: `{plastic_data}`

---

🎯 **Your Task:**
Generate **1 high-potential collaborative product concepts** that could be realistically manufactured and visually promoted.

For each concept, provide:
- **Product Type**: Clear product category (e.g., utility tool, desk item, wearable)
- **Concept Name**: A short, brandable name (4–6 words max)
- **Description**: 40–50 words explaining:
  - What the product is
  - How it fuses both brands (form, story, or material)
  - How the plastic material transforms the function, texture, or aesthetics

---

📌 **Creative & Strategic Constraints:**
- The product **must align with the target brand's market and audience** — adjacent categories are fine if believable.
- The plastic material is **not decorative** — it should meaningfully shape the product (e.g., modularity, tactility, sustainability messaging).
- Emphasize **brand fusion**: combine the **visual/form language** of the target with the **material/innovation ethos** of the source.
- Favor concepts with **strong storytelling or visual distinctiveness** — think of something that could inspire a compelling AI-generated image or pitch deck.

---

🖼️ **Visual/Prompt Guidance** (for downstream AI image generation):
- **Product form** → derives from target brand
- **Material/texture innovation** → derives from source brand
- Think: "How would this look in a premium ad visual?"

Return exactly **1 strong, differentiated idea**.
        """,
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
                  "product_type": "string",
                  "name": "string",
                  "description": "string (30-40 words)"
                }
              ]
            }

            Provide exactly 1 well-considered product concepts.""",
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
