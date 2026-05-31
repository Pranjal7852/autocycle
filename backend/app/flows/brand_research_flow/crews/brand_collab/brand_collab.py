from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from app.utils.crew_logger import CrewLogger
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import logging
import os
import aiohttp
import asyncio
import requests
from app.utils.llm_config import llm_config

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
    estimated_impact: Optional[str] = Field(default=None, description="Potential environmental or market impact formatted as string (e.g., '75M', '1.2B')")
    confidence_score: Optional[int] = Field(default=None, description="Confidence score")
    combined_reach: Optional[str] = Field(default=None, description="Combined marketing reach of both brands formatted as string (e.g., '50M', '2.5B')")
    logo_url: Optional[str] = Field(default=None, description="Brand logo URL from Logo.dev API")
    company_domain: Optional[str] = Field(default=None, description="Brand domain from Logo.dev API")

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
            allow_delegation=False,
            llm=llm_config()
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
            allow_delegation=False,
            llm=llm_config()
        )

    @task
    def identify_collaboration_opportunities(self) -> Task:
        return Task(
            description="""Analyze the provided brand data '{brand_data}', plastic material data '{plastic_data}', location {location}'
and the plastic collaboration direction flag `need_plastic = {need_plastic}`.

Based on the need_plastic flag, apply the following logic:

If need_plastic is True:
- The brand **needs** sustainable plastic to integrate into their product line.
- Recommend collaborators that can **supply**, **upcycle**, or **integrate** their own plastic waste/materials.
- Ensure the plastic is a **core feature** of the proposed product concepts.

If need_plastic is False:
- The brand **provides** sustainable plastic materials (e.g. recycled, upcycled, biodegradable).
- Recommend collaborators that can **utilize** this plastic in their product line meaningfully.
- Ensure that the plastic is **strategically integrated** into the product concept.

Generate up to 5 innovative cross-industry physical product collaboration recommendations.

For each recommendation, provide:
- brand_name: The collaborating brand name
- brand_placement: List of 2-3 key positioning attributes (e.g., ["Premium quality", "Scandinavian design", "Sustainability leader"])
- sustainability_placement: Their current sustainability positioning or commitment
- product_assumptions: List of 2-4 specific physical product concepts that could work (e.g., ["Chair", "Toy", "Shoe"])
- collaboration_summary: 2-3 sentence description explaining the collaboration concept and its strategic value
- estimated_impact: Estimated potential environmental or market impact as a string (e.g., '75M', '2.5B')
- confidence_score: Your confidence in this recommendation on a scale of 1-100
- combined_reach: Combined marketing reach of both brands as a string (e.g., '50M', '100K')

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
      "estimated_impact": "str"
    "confidence_score": "int"
    "combined_reach": "str"
    }
  ]
}

Return up to 5 ideas max. Only include physical products that make sense given the brands and plastic properties.
"""
,
            output_pydantic=CollaborationOutput
        )
    
    @after_kickoff
    def enrich_with_brand_data(self, result):
        """After kickoff hook to enrich collaboration data with brand logos and domains"""
        try:
            logger.logger.info("Executing after kickoff hook - fetching brand logos and domains")
            
            # Extract the collaboration output
            if hasattr(result, 'pydantic') and result.pydantic:
                collaboration_output = result.pydantic
            elif isinstance(result, CollaborationOutput):
                collaboration_output = result
            else:
                logger.logger.warning("Unexpected result format in after kickoff hook")
                return result
            
            # Enrich each collaboration with brand visual data
            for collaboration in collaboration_output.top_collaborations:
                brand_data = self.fetch_brand_logo(collaboration.brand_name)
                if brand_data:
                    collaboration.logo_url = brand_data.get('logo_url')
                    collaboration.company_domain = brand_data.get('company_domain')
                    logger.logger.info(f"Enriched {collaboration.brand_name} with logo and domain data")
                else:
                    logger.logger.warning(f"Could not fetch logo data for {collaboration.brand_name}")
            
            logger.logger.info("After kickoff hook completed successfully")
            return result
            
        except Exception as e:
            logger.logger.error(f"Error in after kickoff hook: {str(e)}")
            # Return original result even if enrichment fails
            return result

    def fetch_brand_logo(self, brand_name: str) -> Optional[Dict[str, str]]:
        """Fetch brand logo and domain data from Logo.dev API"""
        try:
            url = "https://api.logo.dev/search"
            headers = {
                "Authorization": f"Bearer {os.getenv('LOGO_SECRET_KEY')}",
                "Content-Type": "application/json"
            }
            params = {
                "q": brand_name,
        
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract data from first result if available
            if data and len(data) > 0:
                first_result = data[0]
                logo_url = first_result.get("logo_url")
                domain = first_result.get("domain", "")

                if not logo_url:
                    logger.logger.warning(f"No logo URL found for {brand_name}")
                    return None

                # Parse logo_url and add additional params
                url_parts = urlparse(logo_url)
                query_params = dict(parse_qsl(url_parts.query))

                # Add extra parameters
                extra_params = {
                    "retina": "true",
                    "format": "png",
                    "size": "250"
                }
                query_params.update(extra_params)

                # Rebuild URL with updated query params
                new_query = urlencode(query_params)
                updated_logo_url = urlunparse((
                    url_parts.scheme,
                    url_parts.netloc,
                    url_parts.path,
                    url_parts.params,
                    new_query,
                    url_parts.fragment
                ))

                result = {
                    "logo_url": updated_logo_url,
                    "company_domain": domain
                }

                return result
            else:
                logger.logger.warning(f"No logo data found for {brand_name}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.logger.error(f"Network error fetching logo for {brand_name}: {str(e)}")
            return None
        except Exception as e:
            logger.logger.error(f"Error fetching logo for {brand_name}: {str(e)}")
            return None

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