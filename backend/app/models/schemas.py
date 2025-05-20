from pydantic import BaseModel
from typing import List, Dict, Optional

class BrandProfile(BaseModel):
    brand_id: Optional[str] = None
    name: str
    industry: Optional[str] = None
    main_products: List[str]
    sustainability_initiatives: List[str]
    plastic_materials_used: List[str]
    past_collaborations: List[str]
    operational_regions: List[str]

    def to_embedding_text(self) -> str:
        return (
            f"Brand Name: {self.name}\n"
            f"Industry: {self.industry}\n"
            f"Main Products: {', '.join(self.main_products)}\n"
            f"Sustainability Initiatives: {', '.join(self.sustainability_initiatives)}\n"
            f"Plastic Materials Used: {', '.join(self.plastic_materials_used)}\n"
            f"Past Collaborations: {', '.join(self.past_collaborations)}\n"
            f"Operational Regions: {', '.join(self.operational_regions)}"
        )

class PlasticMaterialProfile(BaseModel):
    plastic_id: Optional[str] = None
    type: str
    properties: List[str]
    applications: List[str]
    environmental_impact: str
    recycling_potential: str
    regional_relevance: Optional[str] = ""

    def to_embedding_text(self) -> str:
        return (
            f"Plastic Type: {self.type}\n"
            f"Properties: {', '.join(self.properties)}\n"
            f"Applications: {', '.join(self.applications)}\n"
            f"Environmental Impact: {self.environmental_impact}\n"
            f"Recycling Potential: {self.recycling_potential}\n"
            f"Regional Relevance: {self.regional_relevance}"
        )
