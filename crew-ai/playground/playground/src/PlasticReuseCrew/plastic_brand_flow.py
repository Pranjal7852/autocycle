import asyncio
from typing import List
from crewai.flow.flow import Flow, listen, router, start, and_
from pydantic import BaseModel, Field
from crewai import Agent, Task
from langchain_openai import ChatOpenAI
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlasticBrandState(BaseModel):
    id: str = Field(default_factory=lambda: "")  # Required for CrewAI state ID
    brand_name: str = ""
    plastic_type: str = ""
    location: str = ""
    brand_research: str = ""
    plastic_research: str = ""
    generated_brands: List[str] = []
    selected_brand: str = ""
    product_ideas: str = ""
    creative_pitch: str = ""

class APIInputHandler:
    def __init__(self, state_id, flow_states):
        self.state_id = state_id
        self.flow_states = flow_states

    async def __call__(self, brands):
        prompt = f"Please select a brand concept from the following list:\n" + "\n".join([f"- {brand}" for brand in brands])
        self.flow_states[self.state_id]["prompt"] = prompt
        self.flow_states[self.state_id]["brands"] = brands

        await self.flow_states[self.state_id]["event"].wait()
        self.flow_states[self.state_id]["event"].clear()

        return self.flow_states[self.state_id]["input"]

class PlasticBrandFlow(Flow[PlasticBrandState]):
    initial_state = PlasticBrandState

    def __init__(self, flow_states=None):
        super().__init__()
        self.flow_states = flow_states
        self.llm = ChatOpenAI(model="gpt-4o-mini")

    @start()
    def initialize(self, inputs: dict):
        self.state.brand_name = inputs["brand_name"]
        self.state.plastic_type = inputs["plastic_type"]
        self.state.location = inputs["location"]
        logger.info(f"Flow with State ID {self.state.id} started")
        if self.flow_states:
            self.flow_states[self.state.id]["state_id"] = self.state.id

    @listen(initialize)
    async def research_brand(self):
        logger.info(f"Flow with State ID {self.state.id} researching brand")
        agent = Agent(
            role="Brand Researcher",
            goal="Research the input brand and summarize its market, products, and values.",
            backstory="You are a market analyst with expertise in brand analysis.",
            llm=self.llm
        )
        task = Task(
            description=f"Research the brand '{self.state.brand_name}' in the context of {self.state.location}. Summarize its market position, key products, and core values in 200 words.",
            expected_output="A 200-word summary of the brand's market, products, and values.",
            agent=agent
        )
        result = await task.execute_async()
        self.state.brand_research = result

    @listen(initialize)
    async def research_plastic(self):
        logger.info(f"Flow with State ID {self.state.id} researching plastic")
        agent = Agent(
            role="Plastic Specialist",
            goal="Research the properties and applications of a specific plastic type.",
            backstory="You are a materials scientist specializing in plastics and sustainability.",
            llm=self.llm
        )
        task = Task(
            description=f"Research the plastic type '{self.state.plastic_type}'. Describe its properties, common uses, and sustainability aspects in 200 words.",
            expected_output="A 200-word summary of the plastic's properties, uses, and sustainability.",
            agent=agent
        )
        result = await task.execute_async()
        self.state.plastic_research = result

    @listen(and_(research_brand, research_plastic))
    async def generate_brands(self):
        logger.info(f"Flow with State ID {self.state.id} generating brands")
        agent = Agent(
            role="Brand Innovator",
            goal="Generate creative brand concepts based on a brand and plastic type.",
            backstory="You are a creative director with experience in product branding.",
            llm=self.llm
        )
        task = Task(
            description=f"Using the brand research: '{self.state.brand_research}' and plastic research: '{self.state.plastic_research}', generate 5 new brand concepts or product lines for '{self.state.brand_name}' that leverage '{self.state.plastic_type}'. Each concept should be a single sentence.",
            expected_output="A list of 5 brand or product line concepts, each described in one sentence.",
            agent=agent
        )
        result = await task.execute_async()
        brands = [line.strip("- *12345. ") for line in result.split("\n") if line.strip() and line.startswith(("- ", "* ", "1. ", "2. ", "3. ", "4. ", "5. "))]
        self.state.generated_brands = brands[:5]

    @router(generate_brands)
    async def human_in_the_loop(self):
        logger.info(f"Flow with State ID {self.state.id} waiting for human input")
        input_handler = APIInputHandler(self.state.id, self.flow_states)
        selected_brand = await input_handler(self.state.generated_brands)
        self.state.selected_brand = selected_brand
        logger.info(f"Flow with State ID {self.state.id} selected brand: {selected_brand}")
        return "generate_pitch"

    @listen("generate_pitch")
    async def generate_product_pitch(self):
        logger.info(f"Flow with State ID {self.state.id} generating product pitch")
        agent = Agent(
            role="Product Developer",
            goal="Create product ideas and a creative pitch for a selected brand concept.",
            backstory="You are a product designer and marketing expert with a knack for creative pitches.",
            llm=self.llm
        )
        task = Task(
            description=f"For the selected brand concept '{self.state.selected_brand}' (based on brand '{self.state.brand_name}' and plastic '{self.state.plastic_type}'), generate 3 innovative product ideas and a 150-word creative marketing pitch. Format the output as: 'Product Ideas:\n1. ...\n2. ...\n3. ...\n\nCreative Pitch:\n...'",
            expected_output="A formatted string with 3 product ideas and a 150-word pitch.",
            agent=agent
        )
        result = await task.execute_async()
        parts = result.split("\n\nCreative Pitch:\n")
        if len(parts) == 2:
            self.state.product_ideas = parts[0].replace("Product Ideas:\n", "")
            self.state.creative_pitch = parts[1]
        else:
            self.state.product_ideas = result
            self.state.creative_pitch = "Pitch not generated."

        result = {
            "brand_name": self.state.brand_name,
            "plastic_type": self.state.plastic_type,
            "selected_brand": self.state.selected_brand,
            "product_ideas": self.state.product_ideas,
            "creative_pitch": self.state.creative_pitch,
            "state_id": self.state.id
        }
        logger.info(f"Flow with State ID {self.state.id} completed with result")
        return result

    async def kickoff_async(self, inputs: dict):
        return await self.run(inputs=inputs)