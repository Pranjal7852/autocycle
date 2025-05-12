from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import List
import json
from tools.tools import search_tool, industry_match_tool, image_generator_tool
# try:
#     from tools.tools import search_tool, industry_match_tool
#     print("Successfully imported tools from tools.tools")
# except ImportError:
#     print("Warning: Actual tools not found, using dummy tool placeholders.")
#     search_tool = "dummy_search_tool"
#     industry_match_tool = "dummy_industry_match_tool"

@CrewBase
class PlasticReuseCrew():
    """PlasticReuseCrew orchestrates agents for plastic upcycling analysis."""

    @agent
    def brand_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['brand_analyst'],
            tools=[search_tool],
            verbose=True,
            allow_delegation=True
        )

    @agent
    def industry_matchmaker(self) -> Agent:
        return Agent(
            config=self.agents_config['industry_matchmaker'],
            tools=[industry_match_tool],
            verbose=True,
            allow_delegation=True
        )

    @agent
    def creative_pitch_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_pitch_generator'],
            tools=[industry_match_tool, search_tool],
            verbose=True,
            allow_delegation=True
        )
    
    @agent
    def image_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['image_generator'],
            tools=[image_generator_tool],
            verbose=True,
            allow_delegation=False
        )

    @task
    def analyze_brand_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_brand_task'],
            agent=self.brand_analyst(),
            output_file='brand_analysis_temp.json'  # Temporary file
        )

    @task
    def match_industries_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_industries_task'],
            agent=self.industry_matchmaker(),
            output_file='industry_matches_temp.json',  # Temporary file
            context=[self.analyze_brand_task()]  # Use brand analysis as context
        )

    @task
    def generate_creative_pitches_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_creative_pitches_task'],
            agent=self.creative_pitch_generator(),
            output_file='plastic_reuse_analysis.json',  # Final combined output
            context=[self.analyze_brand_task(), self.match_industries_task()]  # Use both analyses as context
        )
    
    @task
    def generate_image_task(self) -> Task:
        """Generates an image from a product pitch and integrates with the creative pitch task."""
        return Task(
            config=self.tasks_config['generate_image_task'],
            agent=self.image_generator(),
            output_file='generated_image.json',
            context=[self.generate_creative_pitches_task()]  
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PlasticReuseCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True
        )