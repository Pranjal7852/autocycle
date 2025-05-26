from typing import Dict, Optional
import uuid
import logging
from datetime import datetime
from pydantic import BaseModel, validator, ValidationError

from app.database.vector_db import VectorDBManager
from app.database.postgres_db import PostgresManager
from app.models.schemas import BrandProfile
from app.models.schemas import PlasticMaterialProfile
from psycopg2.extras import Json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Pydantic models for input validation


class DataManager:
    def __init__(self):
        self.vector_db = VectorDBManager()
        self.postgres_db = PostgresManager()

    @staticmethod
    def sanitize_input(data):
        if isinstance(data, dict):
            return {k: DataManager.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [DataManager.sanitize_input(i) for i in data]
        elif isinstance(data, datetime):
            return data.isoformat()
        else:
            return data

    def _generate_stable_id(self, namespace: uuid.UUID, name: str) -> str:
        # deterministic UUID based on namespace and name string
        return str(uuid.uuid5(namespace, name.lower()))

    def search_brand(self, brand_name: str) -> Optional[Dict]:
        """
        Search for a brand and return details with similarity score if found
        """
        try:
            results = self.vector_db.search_brand(brand_name.lower(), limit=1)
            print(f"Raw vector DB results for '{brand_name}': {results}")
            if results:
                top_result = results[0]
                brand_id = top_result["brand_id"]
                distance = top_result["distance"]
                similarity_score = max(0.0, min(1.0, 1 - (distance / 2)))  # clamp between 0 and 1

                full_data = self.postgres_db.get_brand_by_id(brand_id)
                if full_data:
                    full_data["similarity_score"] = similarity_score
                    return self.sanitize_input(full_data) if full_data else None
            return None
        except Exception as e:
            logger.error(f"Error searching brand '{brand_name}': {e}")
            return None

    def search_plastic_type(self, plastic_type: str) -> Optional[Dict]:
        """
        Search for a plastic type and return details with similarity score if found
        """
        try:
            results = self.vector_db.search_plastic_type(plastic_type.lower(), limit=1)

            if results:
                top_result = results[0]
                plastic_id = top_result["plastic_id"]
                distance = top_result["distance"]
                similarity_score = max(0.0, min(1.0, 1 - (distance / 2)))

                full_data = self.postgres_db.get_plastic_by_id(plastic_id)
                if full_data:
                    full_data["similarity_score"] = similarity_score
                    return self.sanitize_input(full_data) if full_data else None
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
            brand_model = BrandProfile(**brand_data)
            
            namespace = uuid.UUID('12345678-1234-5678-1234-567812345678')  # Fixed namespace UUID
            brand_id = self._generate_stable_id(namespace, brand_model.name)
            
            if self.vector_db.object_exists("Brand", brand_id):
                logger.info(f"Brand with ID {brand_id} already exists. Skipping insert.")
                return brand_id 

            # Convert model back to dict, update id
            brand_dict = brand_model.model_dump()
            brand_dict["brand_id"] = brand_id
            
            # Store in PostgreSQL
            self.postgres_db.store_brand_data(brand_dict)

            # Store in vector DB
            self.vector_db.add_brand(brand_model, brand_id)

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
            plastic_model = PlasticMaterialProfile(**plastic_data)
            # Generate stable ID if not provided
           
            namespace = uuid.UUID('87654321-4321-8765-4321-876543218765')  # Fixed namespace UUID
            plastic_id = self._generate_stable_id(namespace, plastic_model.type)
            
            plastic_dict = plastic_model.model_dump()
            plastic_dict["plastic_id"] = plastic_id
           
            # Store in PostgreSQL
            self.postgres_db.store_plastic_data(plastic_dict)

            # Store in vector DB
            self.vector_db.add_plastic_type(plastic_model, plastic_id)

            return plastic_id

        except ValidationError as ve:
            logger.error(f"Plastic data validation error: {ve}")
            return None
        except Exception as e:
            logger.error(f"Error adding plastic data: {e}")
            return None
        
    def save_collaboration(self, source_brand: str, target_brand: str, plastic_type: str, location: str) -> int:
        """
        Create a new collaboration entry in the database.
        """
        try:
            collaboration_id = self.postgres_db.create_or_get_collaboration(
                source_brand=source_brand,
                target_brand=target_brand,
                plastic_type=plastic_type,
                location=location
            )
            logger.info(f"Created collaboration with ID: {collaboration_id}")
            return collaboration_id
        except Exception as e:
            logger.error(f"Error saving collaboration: {e}")
            raise

    def save_collaboration_product(self, collaboration_id: int, product_data: Dict) -> int:
        """
        Add a product idea to an existing collaboration in the database.
        """
        try:
            product_id = self.postgres_db.add_collaboration_product(collaboration_id, product_data)
            logger.info(f"Saved collaboration product with ID: {product_id}")
            return product_id
        except Exception as e:
            logger.error(f"Error saving collaboration product: {e}")
            raise

  