from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
from app.flows.brand_research_flow.main import brand_research_kickoff
from app.flows.brand_product_flow.main import brand_product_kickoff
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow POST and OPTIONS for preflight
    allow_headers=["Content-Type"],  # Allow Content-Type header
)
class GenerateBrandRequest(BaseModel):
    brand: str
    plastic_type: str
    location: str

class GenerateProductsRequest(BaseModel):
    source_brand: str
    plastic_type: str
    location: str
    target_brand: str

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
            location=request.location
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
            source_brand=request.source_brand,
            plastic_type=request.plastic_type,
            location=request.location,
            target_brand=request.target_brand
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