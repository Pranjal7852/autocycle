from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict
from crewai_tools import SerperDevTool
from pydantic import BaseModel
from app.utils.crew_logger import CrewLogger

logger = CrewLogger(log_file="crew_execution.log", console_output=True)

# ---------------------------
# ✅ Pydantic Output Model
# ---------------------------

class CollaborationRecommendation(BaseModel):
    name: str
    industry: str
    rationale: str
    product_concept: str

class CollaborationOutput(BaseModel):
    input_summary: Dict[str, str]
    top_collaborating_brands: List[CollaborationRecommendation]


# ---------------------------
# 🚀 Crew Class
# ---------------------------

@CrewBase
class BrandCollabsCrew():
    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.logger = logger

    @agent
    def collaboration_strategist(self) -> Agent:
        return Agent(
            role="Collaboration Strategist",
            goal="Find strong brand collaboration matches using pattern recognition, not heavy research.",
            backstory="""You are a strategic expert in sustainable brand partnerships.
            You match brands with complementary missions and materials.
            You prefer reasoning over searching, and only use one search if absolutely necessary.""",
            tools=[SerperDevTool()],
            verbose=False,
            allow_delegation=False
        )

    @task
    def identify_collaboration_opportunities(self) -> Task:
        return Task(
            description="""You are given two data objects: brand_data and plastic_data.

Use them to recommend 5 strong collaboration candidates.

**DO NOT** search for the brand or plastic. Use what's provided.

Search only once if you need new brands in this format:
"sustainable brands [industry from brand_data] [location if available]"

Look for:
- Complementary industries (not direct competitors)
- Brands with sustainability goals
- Brands that might use the plastic type in their products

Your final output must be structured and insightful.""",
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

    async def kickoff(self, input: Dict) -> CollaborationOutput:
        try:
            if not isinstance(input, dict):
                raise ValueError("Input must be a dictionary")
            if "brand_data" not in input or "plastic_data" not in input:
                raise ValueError("Input must contain 'brand_data' and 'plastic_data'")

            crew_instance = self.crew()
            result = await crew_instance.kickoff_async(inputs=input)

            # Ensure it's converted to a validated Pydantic object
            return CollaborationOutput.parse_obj(result)

        except Exception as e:
            self.logger.error(f"Error in brand collaboration crew: {str(e)}")
            raise
