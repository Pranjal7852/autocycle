from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from crew import PlasticReuseCrew

app = FastAPI(
    title="Plastic Reuse Analysis API",
    description="API for analyzing plastic reuse opportunities using CrewAI",
    version="1.0.0"
)

class AnalysisRequest(BaseModel):
    brand: str
    plastic_type: str
    brand_location: Optional[str] = "Europe"

@app.post("/analyze")
async def analyze_plastic_reuse(request: AnalysisRequest):
    try:
        inputs = {
            'current_year': str(datetime.now().year),
            'brand': request.brand,
            'plastic_type': request.plastic_type,
            'brand location': request.brand_location,
        }
        
        crew = PlasticReuseCrew()
        result = crew.crew().kickoff(inputs=inputs)
        
        return {
            "status": "success",
            "message": "Analysis completed successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during analysis: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 