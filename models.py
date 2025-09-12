from pydantic import BaseModel, Field
from typing import List, Optional

class ElementModel(BaseModel):
    element: str = Field(...)
    reactions_with_heavy_metals: List[str] = Field(...)
    reactions_with_environment: List[str] = Field(...)
    compounds_found: List[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "element": "Titanium (Ti)",
                "reactions_with_heavy_metals": ["Ti + Fe -> FeTi"],
                "reactions_with_environment": ["Ti + O2 -> TiO2"],
                "compounds_found": ["FeTi", "TiO2"]
            }
        }

class UpdateElementModel(BaseModel):
    element: Optional[str]
    reactions_with_heavy_metals: Optional[List[str]]
    reactions_with_environment: Optional[List[str]]
    compounds_found: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "element": "Titanium (Ti)",
                "reactions_with_heavy_metals": ["Ti + Fe -> FeTi", "Ti + Ni -> NiTi"]
            }
        }