from pydantic import BaseModel
from typing import List, Dict, Optional

class BrandProfile(BaseModel):
    brand_id: Optional[str] = None
    name: str
    industry: str
    product_categories: List[str]
    plastic_materials: List[str]
    sustainability_philosophy: Optional[str]
    key_partners_or_collaborators: List[str]
    manufacturing_regions: List[str]
    brand_positioning: Optional[str]

    def to_embedding_text(self) -> str:
        return (
            f"{self.name} is a brand in the {self.industry} industry.\n"
            f"It primarily offers products such as: {', '.join(self.product_categories)}.\n"
            f"The brand uses the following plastic materials: {', '.join(self.plastic_materials)}.\n"
            f"Sustainability philosophy: {self.sustainability_philosophy or 'Not specified'}.\n"
            f"Notable collaborations and partners include: {', '.join(self.key_partners_or_collaborators)}.\n"
            f"Manufacturing and operational regions: {', '.join(self.manufacturing_regions)}.\n"
            f"Its brand positioning is: {self.brand_positioning or 'Not specified'}."
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
