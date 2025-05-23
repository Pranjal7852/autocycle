from pydantic import BaseModel
from crewai.flow import Flow, listen, start, router, and_
from app.crews.brand_analyst.brand_analyst import BrandAnalystCrew
from app.crews.plastic_analyst.plastic_analyst import PlasticAnalystCrew
from app.flows.brand_research_flow.crews.brand_collab.brand_collab import BrandCollabsCrew
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

class BrandResearchState(BaseModel):
    brand_name: str = ""
    plastic_type: str = ""
    location: str = ""
    brand_results: dict = {}
    plastic_results: dict = {}
    collab_results: dict = {}
    combined_results: dict = {}
    brand_research_needed: bool = False
    plastic_research_needed: bool = False
    brand_research_complete: bool = False
    plastic_research_complete: bool = False
    brand_saved_to_db: bool = False
    plastic_saved_to_db: bool = False

class ResearchFlow(Flow[BrandResearchState]):
    def __init__(self, data_manager: DataManager):
        super().__init__()
        logging.info("Initializing Research Flow")
        self.data_manager = data_manager
        self.brand_research_crew = BrandAnalystCrew()
        self.plastic_research_crew = PlasticAnalystCrew()
        self.collab_crew = BrandCollabsCrew()
        self.similarity_threshold = 0.8

    @start()
    async def initialize_research(self):
        logging.info("Initializing research")
        if not self.state.brand_name and not self.state.plastic_type:
            raise ValueError("Either brand_name or plastic_type must be provided")

        await asyncio.gather(
            self.check_brand_database(),
            self.check_plastic_database()
        )
        return {"status": "initialized"}

    async def check_brand_database(self):
        if not self.state.brand_name:
            self.state.brand_research_complete = True
            return

        brand_data = await asyncio.to_thread(
            self.data_manager.search_brand, 
            self.state.brand_name
        )
        self.state.brand_results = brand_data or {}
        similarity = self.state.brand_results.get("similarity_score", 0)
        print(f"vector Search {similarity} for { self.state.brand_name}")
        print(f"vector Search { self.state.brand_name} for { self.state.brand_results}")
        if similarity < self.similarity_threshold:
            self.state.brand_research_needed = True
        else:
            self.state.brand_results["name"] = self.state.brand_name
            self.state.brand_research_complete = True

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
    async def route_brand_research(self):
        if self.state.brand_research_needed:
            return "conduct_brand_research"
        return "brand_research_complete"

    @router(initialize_research)
    async def route_plastic_research(self):
        if self.state.plastic_research_needed:
            return "conduct_plastic_research"
        return "plastic_research_complete"

    @listen("conduct_brand_research")
    async def action_conduct_brand_research(self):
        try:
            input_data = {"brand": self.state.brand_name}
            
            if self.state.location:
                input_data["location"] = self.state.location
            
            result = await self.brand_research_crew.kickoff(input_data=input_data)
        
            self.state.brand_results = result.to_dict()
            self.state.brand_research_complete = True
            # Return the string event name to trigger next step
            return result
        except Exception as e:
            logger.logger.error(f"Error researching brand: {e}")
            return "brand_research_failed"
    
    # Changed to listen for the new event string
    @router(action_conduct_brand_research)
    async def route_after_brand_research(self):
        logger.logger.info(f"Inside Router after research: {self.state.brand_results}")
        try:
            logger.logger.info(f"Storing Brand Info After research: {self.state.brand_results}")
            await self.save_brand_to_db(self.state.brand_results)
            self.state.brand_saved_to_db = True
            return "brand_research_complete"
        except Exception as e:
            logger.logger.error(f"Error storing brand: {e}")
            return {"brand_storing": "failed", "error": str(e)}

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
            await self.save_plastic_to_db(self.state.plastic_results)
            self.state.plastic_saved_to_db = True
            return "plastic_research_complete"
        except Exception as e:
            logger.logger.error(f"Error storing plastic: {e}")
            return {"plastic_storing": "failed", "error": str(e)}
    
    async def save_brand_to_db(self, brand_data: Dict):
        try:
            await self.data_manager.add_brand_data(brand_data)
            self.state.brand_saved_to_db = True
        except Exception as e:
            logger.logger.error(f"Error saving brand to DB: {e}")
            self.state.brand_saved_to_db = False

    async def save_plastic_to_db(self, plastic_data: Dict):
        try:
            await asyncio.to_thread(self.data_manager.add_plastic_data, plastic_data)
            self.state.plastic_saved_to_db = True
        except Exception as e:
            logger.logger.error(f"Error saving plastic to DB: {e}")

    @listen(and_("brand_research_complete", "plastic_research_complete"))
    async def process_collaboration(self):
        try:
            input_data = {
                "brand_data": self.state.brand_results,
                "plastic_data": self.state.plastic_results
            }
            combined_results = await self.collab_crew.kickoff(input_data=input_data)
            self.state.combined_results = combined_results
            return {"status": "collaboration_complete", "results": combined_results}
        except Exception as e:
            logger.logger.error(f"Error in collaboration: {e}")
            return {"status": "collaboration_failed", "error": str(e)}


async def brand_research_kickoff(brand_name: str = "", plastic_type: str = "", location: str = ""):
    data_manager = DataManager()
    flow = ResearchFlow(data_manager)
    flow.state.brand_name = brand_name
    flow.state.plastic_type = plastic_type
    flow.state.location = location
    flow.plot("ResearchFlowPlot")
    logger.logger.info(flow.state)
    return await flow.kickoff_async()