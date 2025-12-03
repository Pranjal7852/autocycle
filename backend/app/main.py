from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
from app.flows.brand_research_flow.main import brand_research_kickoff
from app.flows.brand_product_flow.main import brand_product_kickoff
from fastapi.middleware.cors import CORSMiddleware
from app.database.postgres_db import PostgresManager

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow POST and OPTIONS for preflight
    allow_headers=["Content-Type"],  # Allow Content-Type header
)
class GenerateBrandRequest(BaseModel):
    brand: str
    plastic_type: str
    location: str
    need_plastic: bool

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
            location=request.location,
            need_plastic=request.need_plastic
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
        data_manager = PostgresManager()
        # Step 1: Check existing collaboration
        existing_data = data_manager.get_collaboration_with_products(
            source_brand=request.source_brand,
            target_brand=request.target_brand,
            plastic_type=request.plastic_type,
            location=request.location
        )

        # Step 2: If found and enough products exist, return them
        if existing_data and len(existing_data["products"]) >= 1:
            formatted_products = [
                {
                    "product_name": p["product_name"],
                    "status": "success",
                    "result": {
                        "brand": request.source_brand,
                        "target_brand": request.target_brand,
                        "product_type": p["product_type"],
                        "product_name": p["product_name"],
                        "product_description": p["product_description"],
                        "pitch": p["pitch"],
                        "image_url": p["image_url"]
                    }
                }
                for p in existing_data["products"]
            ]
            return {
                "status": "success",
                "result": {
                    "status": "product_development_complete",
                    "results": formatted_products
                },
                "message": "Retrieved collaboration from database"
            }

        # Step 3: Fallback to AI generation if not enough data
        result = await brand_product_kickoff(
            source_brand=request.source_brand,
            plastic_type=request.plastic_type,
            location=request.location,
            target_brand=request.target_brand
        )

        return {
            "status": "success",
            "result": result,
            "message": "Generated collaboration"
        }

    except Exception as e:
        logger.error(f"Error in generate_products: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
