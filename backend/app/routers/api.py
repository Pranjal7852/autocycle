from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from crews.research_crew.research_crew import ResearchCrew
from crews.report_crew.report_crew import ReportCrew
from flows.main_flow import ContentFlow
from typing import Dict

router = APIRouter(prefix="/api", tags=["CrewAI Endpoints"])

# Input models
class ResearchInput(BaseModel):
    topic: str

class ContentInput(BaseModel):
    topic: str
    audience: str

# Endpoint 1: Research and Report using multiple crews
@router.post("/research-report")
async def research_report(input: ResearchInput) -> Dict:
    try:
        # Initialize research crew
        research_crew = ResearchCrew()
        research_result = research_crew.run(topic=input.topic)
        
        # Pass research output to report crew
        report_crew = ReportCrew()
        report_result = report_crew.run(context=research_result.raw, topic=input.topic)
        
        return {"research": research_result.raw, "report": report_result.raw}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint 2: Content generation using a flow
@router.post("/generate-content")
async def generate_content(input: ContentInput) -> Dict:
    try:
        content_flow = ContentFlow()
        result = content_flow.run(topic=input.topic, audience=input.audience)
        return {"content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
