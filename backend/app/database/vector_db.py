from typing import List
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import weaviate
from weaviate.connect import ConnectionParams
from weaviate.classes.config import Configure, Property, DataType
from weaviate.auth import AuthApiKey

load_dotenv()

class VectorDBManager:
    def __init__(self):
        self.client = None
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self._initialize_client()
        self._create_collections_if_not_exist()

    def _initialize_client(self):
        # Get cloud configuration from environment variables
        weaviate_url = os.getenv("WEAVIATE_URL")
        weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
        weaviate_grpc_port = os.getenv("WEAVIATE_GRPC_PORT")
        weaviate_grpc_url = os.getenv("WEAVIATE_GRPC_URL")
        
        if not weaviate_url or not weaviate_api_key:
            raise ValueError("WEAVIATE_URL and WEAVIATE_API_KEY must be set in environment variables")

        # Initialize client with cloud authentication
        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=AuthApiKey(weaviate_api_key),
        )
        print(self.client.is_ready())

    def _create_collections_if_not_exist(self):
        existing_collections = self.client.collections.list_all()

        if "Brand" not in existing_collections:
            self.client.collections.create(
                name="Brand",
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    Property(name="name", data_type=DataType.TEXT),
                    Property(name="brand_id", data_type=DataType.TEXT),
                ]
            )

        if "PlasticType" not in existing_collections:
            self.client.collections.create(
                name="PlasticType",
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    Property(name="type", data_type=DataType.TEXT),
                    Property(name="plastic_id", data_type=DataType.TEXT),
                ]
            )

    def add_brand(self, brand_name: str, brand_id: str):
        embedding = self.model.encode(brand_name)
        self.client.collections.get("Brand").data.insert(
            properties={
                "name": brand_name,
                "brand_id": brand_id,
            },
            vector=embedding.tolist()
        )

    def add_plastic_type(self, plastic_type: str, plastic_id: str):
        embedding = self.model.encode(plastic_type)
        self.client.collections.get("PlasticType").data.insert(
            properties={
                "type": plastic_type,
                "plastic_id": plastic_id,
            },
            vector=embedding.tolist()
        )

    def search_brand(self, query: str, limit: int = 3):
        query_embedding = self.model.encode(query)
        results = (
            self.client.collections.get("Brand")
            .query.near_vector(
                near_vector=query_embedding.tolist(),  # Pass the list directly
                limit=limit,
                return_properties=["name", "brand_id"],
                return_metadata=["distance"]
            )
        )

        return [
            {
                "name": obj.properties["name"],
                "brand_id": obj.properties["brand_id"],
                "distance": obj.metadata.distance
            }
            for obj in results.objects
        ]

    def search_plastic_type(self, query: str, limit: int = 3):
        query_embedding = self.model.encode(query)
        results = (
        self.client.collections.get("PlasticType")
        .query.near_vector(
            near_vector=query_embedding.tolist(),  # Pass the list directly
            limit=limit,
            return_properties=["type", "plastic_id"],
            return_metadata=["distance"]
        )
        )

        return [
        {
            "type": obj.properties["type"],
            "plastic_id": obj.properties["plastic_id"],
            "distance": obj.metadata.distance
        }
        for obj in results.objects
    ]
