from pydantic import BaseModel
from crewai.flow import Flow, listen, start, router, and_
from app.flows.brand_research_flow.crews.brand_analyst.brand_analyst import BrandAnalystCrew
from app.flows.brand_research_flow.crews.plastic_analyst.plastic_analyst import PlasticAnalystCrew
from app.flows.brand_research_flow.crews.brand_collab.brand_collab import BrandCollabsCrew
from app.utils.db_queries import DataManager
from typing import Dict
import asyncio

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
        print("Initializing Research Flow")
        self.data_manager = data_manager
        self.brand_research_crew = BrandAnalystCrew()
        self.plastic_research_crew = PlasticAnalystCrew()
        self.collab_crew = BrandCollabsCrew()

    @start()
    async def initialize_research(self):
        print("Initializing research")
        if not self.state.brand_name and not self.state.plastic_type:
            raise ValueError("Either brand_name or plastic_type must be provided")
        return {"status": "initialized"}

    @listen(initialize_research)
    async def check_brand_database(self):
        """Check database for brand information if a brand name was provided"""
        if not self.state.brand_name:
            print("No brand name provided, skipping brand search")
            self.state.brand_research_complete = True
            return {"brand_search": "skipped"}
        
        print(f"Searching database for brand: {self.state.brand_name}")
        brand_data = await asyncio.to_thread(
            self.data_manager.search_brand, 
            self.state.brand_name
        )
        
        self.state.brand_results = brand_data or {}
        similarity = self.state.brand_results.get("similarity_score", 0)
        
        if similarity < 0.8:
            print(f"Brand '{self.state.brand_name}' similarity ({similarity}) below 0.8")
            self.state.brand_research_needed = True
        else:
            print(f"Brand '{self.state.brand_name}' found with sufficient similarity ({similarity})")
            self.state.brand_research_complete = True
            
        return {
            "brand_data": self.state.brand_results,
            "brand_research_needed": self.state.brand_research_needed
        }

    @listen(initialize_research)
    async def check_plastic_database(self):
        """Check database for plastic information if a plastic type was provided"""
        if not self.state.plastic_type:
            print("No plastic type provided, skipping plastic search")
            self.state.plastic_research_complete = True
            return {"plastic_search": "skipped"}
        
        print(f"Searching database for plastic: {self.state.plastic_type}")
        plastic_data = await asyncio.to_thread(
            self.data_manager.search_plastic_type, 
            self.state.plastic_type
        )
        
        self.state.plastic_results = plastic_data or {}
        similarity = self.state.plastic_results.get("similarity_score", 0)
        
        if similarity < 0.8:
            print(f"Plastic type '{self.state.plastic_type}' similarity ({similarity}) below 0.8")
            self.state.plastic_research_needed = True
        else:
            print(f"Plastic type '{self.state.plastic_type}' found with sufficient similarity ({similarity})")
            self.state.plastic_research_complete = True
            
        return {
            "plastic_data": self.state.plastic_results,
            "plastic_research_needed": self.state.plastic_research_needed
        }

    @router(check_brand_database)
    async def route_brand_research(self):
        """Route to either brand research or skip based on need"""
        if self.state.brand_research_needed:
            return "conduct_brand_research"
        else:
            self.state.brand_research_complete = True
            return "brand_research_complete"
    
    @router(check_plastic_database)
    async def route_plastic_research(self):
        """Route to either plastic research or skip based on need"""
        if self.state.plastic_research_needed:
            return "conduct_plastic_research"
        else:
            self.state.plastic_research_complete = True
            return "plastic_research_complete"
    
    @listen("conduct_brand_research")
    async def conduct_brand_research(self):
        """Conduct additional brand research"""
        print(f"Researching brand: {self.state.brand_name}")
        try:
            input_data = {"brand": self.state.brand_name}
            if self.state.location:
                input_data["location"] = self.state.location
            print(f"Input data prepared: {input_data}")

            print("Starting crew kickoff...")
            result = await self.brand_research_crew.kickoff(input=input_data)
            print(f"Crew kickoff completed with result: {result}")

            self.state.brand_results = result
            self.state.brand_research_complete = True

            print("Scheduling DB save...")
            asyncio.create_task(self.save_brand_to_db(result))
            print("Returning results...")

            return {"brand_research": "completed", "brand_results": result}
        except Exception as e:
            print(f"Error researching brand: {e}")
            return {"brand_research": "failed", "error": str(e)}
        
    @listen("conduct_plastic_research")
    async def conduct_plastic_research(self):
        """Conduct additional plastic research"""
        print(f"Researching plastic: {self.state.plastic_type}")
        try:
            # Use crew kickoff with input
            input_data = {"plastic_type": self.state.plastic_type}
            if self.state.location:
                input_data["location"] = self.state.location
                
            result = await self.plastic_research_crew.kickoff(input=input_data)
            self.state.plastic_results = result
            self.state.plastic_research_complete = True
            
            # Save to DB in a non-blocking way
            asyncio.create_task(self.save_plastic_to_db(result))
            
            return {"plastic_research": "completed", "plastic_results": result}
        except Exception as e:
            print(f"Error researching plastic: {e}")
            return {"plastic_research": "failed", "error": str(e)}
            
    async def save_brand_to_db(self, brand_data: Dict):
        """Save brand data to database"""
        try:
            await asyncio.to_thread(self.data_manager.add_brand_data, brand_data)
            self.state.brand_saved_to_db = True
            print(f"Brand '{brand_data.get('name', '')}' saved to database")
        except Exception as e:
            print(f"Error saving brand to database: {e}")
            
    async def save_plastic_to_db(self, plastic_data: Dict):
        """Save plastic data to database"""
        try:
            await asyncio.to_thread(self.data_manager.add_plastic_data, plastic_data)
            self.state.plastic_saved_to_db = True
            print(f"Plastic '{plastic_data.get('type', '')}' saved to database")
        except Exception as e:
            print(f"Error saving plastic to database: {e}")

    @listen(and_("brand_research_complete", "plastic_research_complete"))
    async def process_collaboration(self):
        """Process collaboration only when both research paths are complete"""
        # Double-check that both research paths are marked as complete
        if not self.state.brand_research_complete and self.state.brand_name:
            print("Brand research not complete yet, waiting...")
            return {"status": "waiting_for_brand_research"}
            
        if not self.state.plastic_research_complete and self.state.plastic_type:
            print("Plastic research not complete yet, waiting...")
            return {"status": "waiting_for_plastic_research"}
        
        print("All research complete, processing collaboration")
        try:
            # Use crew kickoff with input
            input_data = {
                "brand_data": self.state.brand_results,
                "plastic_data": self.state.plastic_results
            }
            
            combined_results = await self.collab_crew.kickoff(input=input_data)
            self.state.combined_results = combined_results
            return {"status": "collaboration_complete", "results": combined_results}
        except Exception as e:
            print(f"Error in collaboration processing: {e}")
            return {"status": "collaboration_failed", "error": str(e)}


async def kickoff(brand_name: str = "", plastic_type: str = "", location: str = ""):
    data_manager = DataManager()
    flow = ResearchFlow(data_manager)
    flow.state.brand_name = brand_name
    flow.state.plastic_type = plastic_type
    flow.state.location = location
    print(flow.state)
    return await flow.kickoff_async()