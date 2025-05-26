import asyncio
import os
import logging
from pydantic import BaseModel
from typing import List, Dict
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from app.utils.crew_logger import CrewLogger
from crewai_tools import SerperDevTool
from app.flows.brand_product_flow.crews.brand_product_developer.tools.image_generator import generate_image_via_openai

# Setup logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'product_image_crew.log')

logger = CrewLogger(
    log_file=log_file,
    log_level=logging.DEBUG,
    console_output=True
)

# Output model
class ProductOutput(BaseModel):
    pitch: str
    image_url: str

@CrewBase
class BrandProductDevelopers:

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.logger = logger

    def pitch_writer(self, brand: str, target_brand: str, product_name: str, product_type: str) -> Agent:
        return Agent(
            role="Creative Pitch Generator",
            goal=f"Generate a compelling product pitch for {product_name}, an upcycled {product_type}, highlighting {target_brand}'s market positioning.",
            backstory=f"""You are a creative strategist skilled at:
            - Developing sustainable and innovative product concepts
            - Creating marketing pitches that align with brand values
            - Envisioning co-branded opportunities between {brand} and {target_brand}""",
            verbose=True
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[],  # Will dynamically create agents per product
            tasks=[],
            process=Process.sequential,
            verbose=True
        )

    async def kickoff(self, input_data: Dict) -> Dict:
        try:
            logger.logger.info(f"Kicking off BrandProductDevelopers with input: {input_data}")

            brand = input_data["brand"]
            target_brand = input_data["target_brand"]
            product_name = input_data["product_name"]
            product_type = input_data.get("product_type", "")
            product_description = input_data.get("product_description", "")

            pitch_agent = self.pitch_writer(brand, target_brand, product_name, product_type)

            pitch_prompt = f"""
            Generate a pitch for an upcycled {product_type} called "{product_name}", a collaboration between {brand} and {target_brand}.
            
            this is the discription about the product - {product_description}

            Include:
            - A detailed concept (10-20 words)
            - How it leverages each brand's identity
            - Market positioning and intended audience
            - Sustainability innovation
            - Co-branding and storytelling potential
            
            """

            image_prompt = f"""
            Create a high-quality product image of the {product_type} named "{product_name}".
            Visualize collaboration between {brand} and {target_brand}.
            Requirements:
            - Realistic editorial style image
            - Modern commercial tones (pastels or bold neutrals)
            - Soft lighting and natural shadows
            - Include text "{brand} X {target_brand}" but no logos
            """

            # Define the pitch task
            pitch_task = Task(
                description=pitch_prompt,
                expected_output="A structured, creative pitch.",
                agent=pitch_agent
            )

            # Create a temporary crew for the pitch generation
            pitch_crew = Crew(
                agents=[pitch_agent],
                tasks=[pitch_task],
                process=Process.sequential,
                verbose=True
            )

            pitch_result = await pitch_crew.kickoff_async()

            # Run image generation concurrently
            image_task = asyncio.to_thread(
                generate_image_via_openai,
                prompt=image_prompt,
                product_name=product_name
            )

            image_url = await image_task

            result = {
                "brand": brand,
                "target_brand": target_brand,
                "product_type": product_type,
                "product_name": product_name,
                "product_description": product_description,
                "pitch": pitch_result.raw,
                "image_url": image_url
            }

            logger.logger.info(f"Product development completed: {result}")
            return result

        except Exception as e:
            logger.logger.error(f"Error in BrandProductDevelopers kickoff: {str(e)}")
            return {
                "status": "product_development_failed",
                "error": str(e)
            }
