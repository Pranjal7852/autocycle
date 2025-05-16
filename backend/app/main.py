from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
from app.flows.brand_research_flow.main import kickoff

load_dotenv()

app = FastAPI()

class GenerateBrandRequest(BaseModel):
    brand: str
    plastic_type: str
    brand_location: str

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI for Python!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generateBrand")
async def analyze_plastic_reuse(request: GenerateBrandRequest):
    try:
        # Run the brand research flow
        result = await kickoff(
            brand_name=request.brand,
            plastic_type=request.plastic_type,
            location=request.brand_location
        )
        
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }