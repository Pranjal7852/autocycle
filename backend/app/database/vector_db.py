from typing import List
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import weaviate
from weaviate.connect import ConnectionParams
from weaviate.classes.config import Configure, Property, DataType
from weaviate.auth import AuthApiKey
from app.flows.brand_research_flow.crews.brand_analyst.brand_analyst import BrandProfile
from app.flows.brand_research_flow.crews.plastic_analyst.plastic_analyst import PlasticMaterialProfile
import logging

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
            skip_init_checks=True
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

    def object_exists(self, collection_name: str, object_id: str) -> bool:
        try:
            collection = self.client.collections.get(collection_name)
            result = collection.query.fetch_object_by_id(object_id)
            print(f"object exist result", result)
            return result is not None  # Or: return bool(result)
        except Exception as e:
            print(f"Error checking object existence in Weaviate: {e}")
            return False

    def add_brand(self, brand_model: BrandProfile, brand_id: str):
        embedding_text = brand_model.to_embedding_text().lower()
        embedding = self.model.encode(embedding_text)
        print("VECTORDB INSERT DEBUG - brand_data:", {
            "name": brand_model.name.lower(),
            "brand_id": brand_id,
            "embedding_text": embedding_text
        })
        self.client.collections.get("Brand").data.insert(
        uuid=brand_id,
        properties={
            "name": brand_model.name.lower(),
            "brand_id": brand_id,
            "embedding_text": embedding_text 
        },
        vector=embedding.tolist()
        )

    def add_plastic_type(self, plastic_model: PlasticMaterialProfile, plastic_id: str):
        embedding_text = plastic_model.to_embedding_text().lower()
        embedding = self.model.encode(embedding_text)
        collection = self.client.collections.get("PlasticType")
        
        try:
            existing_object = collection.query.fetch_object_by_id(plastic_id)
            if existing_object:
                logging.info(f"Plastic type with UUID {plastic_id} exists. Updating.")
                collection.data.update(
                    uuid=plastic_id,
                    properties={
                        "name": plastic_model.type.lower(),
                        "plastic_id": plastic_id,
                        "embedding_text": embedding_text
                    },
                    vector=embedding.tolist()
                )
                return
        except Exception as e:
            logging.error(f"Failed to update plastic type with UUID {plastic_id}: {e}")
            raise

        try:
            collection.data.insert(
                uuid=plastic_id,
                properties={
                    "name": plastic_model.type.lower(),
                    "plastic_id": plastic_id,
                    "embedding_text": embedding_text
                },
                vector=embedding.tolist()
            )
            logging.info(f"Inserted plastic type with UUID {plastic_id}")
        except Exception as e:
            logging.error(f"Failed to insert plastic type with UUID {plastic_id}: {e}")
            raise

    def search_brand(self, query: str, limit: int = 3):
        embedding_text = (
    f"{query.lower()} is a global brand in its respective industry.\n"
    f"It offers products or services aligned with its market positioning.\n"
    f"It may use or recycle plastic materials in its operations.\n"
    f"It could be engaged in sustainability initiatives or ESG practices.\n"
    f"It may collaborate with other brands or suppliers.\n"
    f"It operates in specific regional or global markets.\n"
    f"Its brand positioning may be premium, eco-conscious, or mainstream."
)
        query_embedding = self.model.encode(embedding_text)
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
        embedding_text = f"Plastic type: {query}".lower()  
        query_embedding = self.model.encode(embedding_text)
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
