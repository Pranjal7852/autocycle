from typing import Dict, Optional
import uuid
import logging
from pydantic import BaseModel, validator, ValidationError

from app.database.vector_db import VectorDBManager
from app.database.postgres_db import PostgresManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Pydantic models for input validation

class BrandDataModel(BaseModel):
    brand_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    sustainability_score: Optional[float] = None
    recycling_info: Optional[str] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Brand name must be a non-empty string")
        return v.strip()

class PlasticDataModel(BaseModel):
    plastic_id: Optional[str] = None
    type: str
    description: Optional[str] = None
    recyclable: Optional[bool] = None
    biodegradable: Optional[bool] = None
    decomposition_time: Optional[str] = None

    @validator('type')
    def type_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Plastic type must be a non-empty string")
        return v.strip()

class DataManager:
    def __init__(self):
        self.vector_db = VectorDBManager()
        self.postgres_db = PostgresManager()

    def _generate_stable_id(self, namespace: uuid.UUID, name: str, prefix: str) -> str:
        # deterministic UUID based on namespace and name string
        return f"{prefix}_{uuid.uuid5(namespace, name)}"

    def search_brand(self, brand_name: str) -> Optional[Dict]:
        """
        Search for a brand and return details with similarity score if found
        """
        try:
            results = self.vector_db.search_brand(brand_name, limit=1)

            if results:
                top_result = results[0]
                brand_id = top_result["brand_id"]
                distance = top_result["distance"]
                similarity_score = max(0.0, min(1.0, 1 - distance))  # clamp between 0 and 1

                full_data = self.postgres_db.get_brand_by_id(brand_id)
                if full_data:
                    full_data["similarity_score"] = similarity_score
                    return full_data
            return None
        except Exception as e:
            logger.error(f"Error searching brand '{brand_name}': {e}")
            return None

    def search_plastic_type(self, plastic_type: str) -> Optional[Dict]:
        """
        Search for a plastic type and return details with similarity score if found
        """
        try:
            results = self.vector_db.search_plastic_type(plastic_type, limit=1)

            if results:
                top_result = results[0]
                plastic_id = top_result["plastic_id"]
                distance = top_result["distance"]
                similarity_score = max(0.0, min(1.0, 1 - distance))

                full_data = self.postgres_db.get_plastic_by_id(plastic_id)
                if full_data:
                    full_data["similarity_score"] = similarity_score
                    return full_data
            return None
        except Exception as e:
            logger.error(f"Error searching plastic type '{plastic_type}': {e}")
            return None

    def add_brand_data(self, brand_data: Dict) -> Optional[str]:
        """
        Add brand data to both PostgreSQL and vector DB
        """
        try:
            # Validate input data
            brand_model = BrandDataModel(**brand_data)
            
            # Generate stable ID if not provided
            if not brand_model.brand_id:
                namespace = uuid.UUID('12345678-1234-5678-1234-567812345678')  # Fixed namespace UUID
                brand_id = self._generate_stable_id(namespace, brand_model.name, "brand")
            else:
                brand_id = brand_model.brand_id

            # Convert model back to dict, update id
            brand_dict = brand_model.dict()
            brand_dict["brand_id"] = brand_id
            
            # Store in PostgreSQL
            self.postgres_db.store_brand_data(brand_dict)

            # Store in vector DB
            self.vector_db.add_brand(brand_dict["name"], brand_id)

            return brand_id

        except ValidationError as ve:
            logger.error(f"Brand data validation error: {ve}")
            return None
        except Exception as e:
            logger.error(f"Error adding brand data: {e}")
            return None

    def add_plastic_data(self, plastic_data: Dict) -> Optional[str]:
        """
        Add plastic type data to both PostgreSQL and vector DB
        """
        try:
            # Validate input data
            plastic_model = PlasticDataModel(**plastic_data)
            
            # Generate stable ID if not provided
            if not plastic_model.plastic_id:
                namespace = uuid.UUID('87654321-4321-8765-4321-876543218765')  # Fixed namespace UUID
                plastic_id = self._generate_stable_id(namespace, plastic_model.type, "plastic")
            else:
                plastic_id = plastic_model.plastic_id

            plastic_dict = plastic_model.dict()
            plastic_dict["plastic_id"] = plastic_id
            
            # Store in PostgreSQL
            self.postgres_db.store_plastic_data(plastic_dict)

            # Store in vector DB
            self.vector_db.add_plastic_type(plastic_dict["type"], plastic_id)

            return plastic_id

        except ValidationError as ve:
            logger.error(f"Plastic data validation error: {ve}")
            return None
        except Exception as e:
            logger.error(f"Error adding plastic data: {e}")
            return None
