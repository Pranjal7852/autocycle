from typing import Dict
from app.database.vector_db import VectorDBManager
from app.database.postgres_db import PostgresManager

class DataManager:
    def __init__(self):
        self.vector_db = VectorDBManager()
        self.postgres_db = PostgresManager()
    
    def search_brand(self, brand_name: str):
        """
        Search for a brand and return details with similarity score if found
        """
        # Search in vector DB first
        results = self.vector_db.search_brand(brand_name, limit=1)
        
        if results:
            # Get the most similar result
            top_result = results[0]
            brand_id = top_result["brand_id"]
            distance = top_result["distance"]
            similarity_score = 1 - distance  # Convert distance to similarity
            
            # Fetch complete data from PostgreSQL
            full_data = self.postgres_db.get_brand_by_id(brand_id)
            if full_data:
                full_data["similarity_score"] = similarity_score
                return full_data
        
        return None
    
    def search_plastic_type(self, plastic_type: str):
        """
        Search for a plastic type and return details with similarity score if found
        """
        # Search in vector DB first
        results = self.vector_db.search_plastic_type(plastic_type, limit=1)
        
        if results:
            # Get the most similar result
            top_result = results[0]
            plastic_id = top_result["plastic_id"]
            distance = top_result["distance"]
            similarity_score = 1 - distance  # Convert distance to similarity
            
            # Fetch complete data from PostgreSQL
            full_data = self.postgres_db.get_plastic_by_id(plastic_id)
            if full_data:
                full_data["similarity_score"] = similarity_score
                return full_data
        
        return None
    
    def add_brand_data(self, brand_data: Dict):
        """
        Add brand data to both PostgreSQL and vector DB
        """
        # Store in PostgreSQL first
        brand_id = brand_data.get("brand_id", f"brand_{hash(brand_data.get('name', ''))}")
        brand_data["brand_id"] = brand_id
        
        self.postgres_db.store_brand_data(brand_data)
        
        # Store in vector DB for searching
        self.vector_db.add_brand(brand_data["name"], brand_id)
        
        return brand_id
    
    def add_plastic_data(self, plastic_data: Dict):
        """
        Add plastic type data to both PostgreSQL and vector DB
        """
        # Store in PostgreSQL first
        plastic_id = plastic_data.get("plastic_id", f"plastic_{hash(plastic_data.get('type', ''))}")
        plastic_data["plastic_id"] = plastic_id
        
        self.postgres_db.store_plastic_data(plastic_data)
        
        # Store in vector DB for searching
        self.vector_db.add_plastic_type(plastic_data["type"], plastic_id)
        
        return plastic_id