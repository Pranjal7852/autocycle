from pydantic import BaseModel
from crewai.flow import Flow, listen, start, router, and_
from app.flows.brand_research_flow.crews.brand_analyst.brand_analyst import BrandAnalystCrew
from app.flows.brand_research_flow.crews.plastic_analyst.plastic_analyst import PlasticAnalystCrew
from app.flows.brand_research_flow.crews.brand_collab.brand_collab import BrandCollabsCrew
from app.utils.db_queries import DataManager
from typing import Dict
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

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
    async def conduct_brand_research(self):
        try:
            input_data = {"brand": self.state.brand_name}
            if self.state.location:
                input_data["location"] = self.state.location

            result = await self.brand_research_crew.kickoff(input_data=input_data)
        
            self.state.brand_results = result
            self.state.brand_research_complete = True
            asyncio.create_task(self.save_brand_to_db(result.to_dict()))
            return "brand_research_complete"
        except Exception as e:
            logging.error(f"Error researching brand: {e}")
            return {"brand_research": "failed", "error": str(e)}

    @listen("conduct_plastic_research")
    async def conduct_plastic_research(self):
        try:
            input_data = {"plastic_type": self.state.plastic_type}
            if self.state.location:
                input_data["location"] = self.state.location

            result = await self.plastic_research_crew.kickoff(input_data=input_data)
            self.state.plastic_results = result
            self.state.plastic_research_complete = True
            asyncio.create_task(self.save_plastic_to_db(result.to_dict()))
            return "plastic_research_complete"
        except Exception as e:
            logging.error(f"Error researching plastic: {e}")
            return {"plastic_research": "failed", "error": str(e)}

    async def save_brand_to_db(self, brand_data: Dict):
        try:
            logging.debug(f"CrewOutput: {brand_data}")
            logging.debug(f"CrewOutput attributes: {dir(brand_data)}")
            logging.debug(f"Raw: {getattr(brand_data, 'raw', None)}")
            logging.debug(f"JSON Dict: {getattr(brand_data, 'json_dict', None)}")
            logging.debug(f"Pydantic: {getattr(brand_data, 'pydantic', None)}")
            logging.debug(f"Tasks Output: {getattr(brand_data, 'tasks_output', None)}")
            await asyncio.to_thread(self.data_manager.add_brand_data, brand_data)
            self.state.brand_saved_to_db = True
        except Exception as e:
            logging.error(f"Error saving brand to DB: {e}")
            self.state.brand_saved_to_db = False

    async def save_plastic_to_db(self, plastic_data: Dict):
        try:
            await asyncio.to_thread(self.data_manager.add_plastic_data, plastic_data)
            self.state.plastic_saved_to_db = True
        except Exception as e:
            logging.error(f"Error saving plastic to DB: {e}")

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
            logging.error(f"Error in collaboration: {e}")
            return {"status": "collaboration_failed", "error": str(e)}


async def kickoff(brand_name: str = "", plastic_type: str = "", location: str = ""):
    data_manager = DataManager()
    flow = ResearchFlow(data_manager)
    flow.state.brand_name = brand_name
    flow.state.plastic_type = plastic_type
    flow.state.location = location
    flow.plot("ResearchFlowPlot")
    logging.info(flow.state)
    return await flow.kickoff_async()
