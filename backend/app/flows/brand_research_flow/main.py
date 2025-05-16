#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from app.flows.brand_research_flow.crews.brand_analyst.brand_analyst import BrandAnalystCrew
import asyncio


class BrandResearchState(BaseModel):
    brand_name: str = ""
    plastic_type: str = ""
    location: str = ""
    research_results: str = ""


class BrandResearchFlow(Flow[BrandResearchState]):

    @start()
    def initialize_research(self):
        print("Initializing brand research")
        # Values are now set through kickoff from API request

    @listen(initialize_research)
    async def conduct_research(self):
        print("Conducting brand research")
        crew = BrandAnalystCrew().crew()
        result = await crew.kickoff_async(
            inputs={
                "brand": self.state.brand_name,
                "plastic_type": self.state.plastic_type,
                "location": self.state.location
            }
        )

        print("Research completed", result.raw)
        self.state.research_results = result.raw

    @listen(conduct_research)
    def save_research(self):
        print("Saving research results")
        with open("brand_research_results.txt", "w") as f:
            f.write(self.state.research_results)


async def kickoff(brand_name: str, plastic_type: str, location: str):
    brand_flow = BrandResearchFlow()
    brand_flow.state.brand_name = brand_name
    brand_flow.state.plastic_type = plastic_type
    brand_flow.state.location = location
    # Run the flow in a thread pool to avoid blocking
    return await asyncio.to_thread(brand_flow.kickoff)

# Uncomment this when you want to plot the flow
# def plot():
#     brand_flow = BrandResearchFlow()
#     brand_flow.plot()


