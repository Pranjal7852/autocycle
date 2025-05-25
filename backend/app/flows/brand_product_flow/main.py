from pydantic import BaseModel
from typing import List
from crewai.flow import Flow, listen, start, router, and_
from app.crews.brand_analyst.brand_analyst import BrandAnalystCrew
from app.crews.plastic_analyst.plastic_analyst import PlasticAnalystCrew
from app.flows.brand_product_flow.crews.brand_product_ideas.brand_product_ideas import BrandProductIdeasCrew
from app.flows.brand_product_flow.crews.brand_product_developer.brand_product_developer import BrandProductDevelopers
from app.utils.db_queries import DataManager
from typing import Dict
import asyncio
import os
import logging
from app.utils.crew_logger import CrewLogger

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'crew_execution.log')

logger = CrewLogger(
    log_file=log_file,
    log_level=logging.DEBUG,
    console_output=True
)

class BrandProductState(BaseModel):
    source_brand: str = ""
    plastic_type: str = ""
    location: str = ""
    target_brand: str = ""

    source_brand_results: dict = {}
    target_brand_results: dict = {}
    plastic_results: dict = {}

    product_ideas: List[dict] = []
    product_pitches: List[str] = []
    product_images: List[str] = []

    source_brand_research_needed: bool = False
    target_brand_research_needed: bool = False
    source_brand_research_complete: bool = False
    target_brand_research_complete: bool = False

    
    plastic_research_needed: bool = False
    plastic_research_complete: bool = False
    collaboration_complete: bool = False

    source_brand_saved_to_db: bool = False
    target_brand_saved_to_db: bool = False
    plastic_saved_to_db: bool = False

class BrandProductFlow(Flow[BrandProductState]):
    def __init__(self, data_manager: DataManager):
        super().__init__()
        logging.info("Initializing Research Flow")
        self.data_manager = data_manager
        self.brand_research_crew = BrandAnalystCrew()
        self.plastic_research_crew = PlasticAnalystCrew()
        self.ideator_crew = BrandProductIdeasCrew()
        self.product_crew = BrandProductDevelopers()
        self.similarity_threshold = 0.8

    @start()
    async def initialize_research(self):
        logging.info("Initializing research")
        if not self.state.source_brand and not self.state.target_brand and not self.state.source_plastic:
            raise ValueError("At least one of source_brand, target_brand, or plastic_type must be provided")

        await asyncio.gather(
            self.check_brand_database(self.state.source_brand, "source"),
            self.check_brand_database(self.state.target_brand, "target"),
            self.check_plastic_database()
        )
        return {"status": "initialized"}

    async def check_brand_database(self, brand_name: str, role: str):
        if not brand_name:
            setattr(self.state, f"{role}_brand_research_complete", True)
            return

        brand_data = await asyncio.to_thread(
            self.data_manager.search_brand, 
            brand_name
        )
        similarity = (brand_data or {}).get("similarity_score", 0)
        print(f"[{role}] vector similarity for '{brand_name}': {similarity}")

        if similarity < self.similarity_threshold:
            setattr(self.state, f"{role}_brand_research_needed", True)
        else:
            if brand_data:
                brand_data["name"] = brand_name
            setattr(self.state, f"{role}_brand_results", brand_data)
            setattr(self.state, f"{role}_brand_research_complete", True)

    async def check_plastic_database(self):
        if not self.state.plastic_type:
            self.state.plastic_research_complete = True
            return

        plastic_data = await asyncio.to_thread(
            self.data_manager.search_plastic_type, 
            self.state.plastic_type
        )
        self.state.plastic_results = plastic_data or {}
        similarity = self.state.plastic_results.get("similarity_score", 0)
        print(f"vector Search {similarity} for plastic { self.state.plastic_type}")
        print(f"vector Search { self.state.plastic_type} for { self.state.plastic_results}")
        if similarity < self.similarity_threshold:
            self.state.plastic_research_needed = True
        else:
            self.state.plastic_research_complete = True

    @router(initialize_research)
    async def route_source_brand_research(self):
        return "conduct_source_brand_research" if self.state.source_brand_research_needed else "source_brand_research_complete"

    @router(initialize_research)
    async def route_target_brand_research(self):
        return "conduct_target_brand_research" if self.state.target_brand_research_needed else "target_brand_research_complete" 

    @router(initialize_research)
    async def route_plastic_research(self):
        if self.state.plastic_research_needed:
            return "conduct_plastic_research"
        return "plastic_research_complete"

    @listen("conduct_source_brand_research")
    async def action_conduct_source_brand_research(self):
        try:
            input_data = {"brand": self.state.source_brand}
            
            if self.state.location:
                input_data["location"] = self.state.location
            
            result = await self.brand_research_crew.kickoff(input_data=input_data)
        
            self.state.source_brand_results = result.to_dict()
            self.state.source_brand_research_complete = True
            # Return the string event name to trigger next step
            return result
        except Exception as e:
            logger.logger.error(f"Error researching source brand: {e}")
            return "source_brand_research_failed"
    
    @router("action_conduct_source_brand_research")
    async def route_after_source_brand_research(self):
        logger.logger.info(f"Inside Router after research: {self.state.source_brand_results}")
        try:
            logger.logger.info(f"Storing Brand Info After research: {self.state.source_brand_results}")
            self.data_manager.add_brand_data(self.state.source_brand_results)
            self.state.source_brand_saved_to_db = True
            return "source_brand_research_complete"
        except Exception as e:
            logger.logger.error(f"Error storing source brand: {e}")
            return {"source_brand_storing": "failed", "error": str(e)}
        
    @listen("conduct_target_brand_research")
    async def action_conduct_target_brand_research(self):
        try:
            input_data = {"brand": self.state.target_brand}
            
            if self.state.location:
                input_data["location"] = self.state.location
            result = await self.brand_research_crew.kickoff(input_data=input_data)
            self.state.target_brand_results = result.to_dict()
            self.state.target_brand_research_complete = True
            # Return the string event name to trigger next step
            return result
        except Exception as e:
            logger.logger.error(f"Error researching target brand: {e}")
            return "target_brand_research_failed"
    
    
    @router(action_conduct_target_brand_research)
    async def route_after_target_brand_research(self):
        logger.logger.info(f"Inside Router after research: {self.state.target_brand_results}")
        try:
            logger.logger.info(f"Storing Brand Info After research: {self.state.target_brand_results}")
            self.data_manager.add_brand_data(self.state.target_brand_results)
            self.state.target_brand_saved_to_db = True
            return "target_brand_research_complete"
        except Exception as e:
            logger.logger.error(f"Error storing target brand: {e}")
            return {"target_brand_storing": "failed", "error": str(e)}

    @listen("conduct_plastic_research")
    async def action_conduct_plastic_research(self):
        try:
            input_data = {"plastic_type": self.state.plastic_type}
            if self.state.location:
                input_data["location"] = self.state.location

            result = await self.plastic_research_crew.kickoff(input_data=input_data)
            self.state.plastic_results = result.to_dict()
            self.state.plastic_research_complete = True
            # Return a different signal to indicate research is done
            return result
        except Exception as e: 
            logger.logger.error(f"Error researching plastic: {e}")
            return {"plastic_research": "failed", "error": str(e)}

    # Changed to listen for the new status signal
    @router(action_conduct_plastic_research)
    async def route_after_plastic_research(self):
        logger.logger.info(f"Inside Router after plastic research: {self.state.plastic_results}")
        try:
            logger.logger.info(f"Storing Plastic Info After research: {self.state.plastic_results}")
            self.data_manager.add_plastic_data(self.state.plastic_results)
            self.state.plastic_saved_to_db = True
            return "plastic_research_complete"
        except Exception as e:
            logger.logger.error(f"Error storing plastic: {e}")
            return {"plastic_storing": "failed", "error": str(e)}
    

    @listen(and_("source_brand_research_complete","target_brand_research_complete", "plastic_research_complete"))
    async def process_product_ideas(self):
        try:
            input_data = {
                "source_brand_data": self.state.source_brand_results,
                "target_brand_data": self.state.target_brand_results,
                "plastic_data": self.state.plastic_results
            }
            combined_results = await self.ideator_crew.kickoff(input_data=input_data)
            self.state.product_ideas = combined_results
            return combined_results
        except Exception as e:
            logger.logger.error(f"Error in product ideas: {e}")
            return {"status": "product_ideas_failed", "error": str(e)}

    @listen("process_product_ideas")
    async def process_product_development_v2(self):
        try:
            product_ideas = self.state.product_ideas["products"]
            
            # Create coroutines for parallel execution
            coroutines = [
                self.product_crew.kickoff({
                    "brand": self.state.source_brand,
                    "target_brand": self.state.target_brand,
                    "product_type": product.get("product_type", ""),
                    "product_name": product["name"],
                    "product_description": product.get("description", "")
                })
                for product in product_ideas
            ]
            
            # Execute all coroutines in parallel
            all_results = await asyncio.gather(*coroutines, return_exceptions=True)
            
            # Process results
            processed_results = []
            for i, result in enumerate(all_results):
                if isinstance(result, Exception):
                    processed_results.append({
                        "product_name": product_ideas[i]["name"],
                        "status": "failed",
                        "error": str(result)
                    })
                else:
                    processed_results.append({
                        "product_name": product_ideas[i]["name"],
                        "status": "success",
                        "result": result
                    })

            return {
                "status": "product_development_complete",
                "results": processed_results
            }
        except Exception as e:
            logger.logger.error(f"Error in product development: {e}")
            return {
                "status": "product_development_failed",
                "error": str(e)
            }

async def brand_product_kickoff(source_brand: str = "", plastic_type: str = "", location: str = "", target_brand: str = ""):
    data_manager = DataManager()
    flow = BrandProductFlow(data_manager)
    flow.state.source_brand = source_brand
    flow.state.plastic_type = plastic_type
    flow.state.location = location
    flow.state.target_brand = target_brand
    flow.plot("BrandProductFlowPlot")
    logger.logger.info(flow.state)
    return await flow.kickoff_async()