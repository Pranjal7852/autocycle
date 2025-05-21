from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
from app.flows.brand_research_flow.main import brand_research_kickoff
from app.flows.brand_product_flow.main import brand_product_kickoff

load_dotenv()

app = FastAPI()

class GenerateBrandRequest(BaseModel):
    brand: str
    plastic_type: str
    brand_location: str

class GenerateProductsRequest(BaseModel):
    SourceBrand: str
    SourcePlastic: str
    SourceLocation: str
    TargetBrand: str

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI for Python!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generatebrand")
async def analyze_plastic_reuse(request: GenerateBrandRequest):
    try:
        # Run the brand research flow
        result = await brand_research_kickoff(
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

@app.post("/generateproducts")
async def generate_products(request: GenerateProductsRequest):
    try:
        # Run the brand research flow
        result = await brand_product_kickoff(
            source_brand=request.SourceBrand,
            source_plastic=request.SourcePlastic,
            source_location=request.SourceLocation,
            target_brand=request.TargetBrand
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