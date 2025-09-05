from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
from engine import HealthImpactEngine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Health Impact Engine API",
    description="API for evaluating health risks from heavy metals in water samples",
    version="1.0.0"
)

# Initialize the engine
try:
    engine = HealthImpactEngine()
    logger.info("Health Impact Engine initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize engine: {e}")
    engine = None

# Pydantic models for request/response
class WaterSampleInput(BaseModel):
    """Input model for water sample data."""
    # Location info (optional)
    Location: Optional[str] = None
    State: Optional[str] = None
    District: Optional[str] = None
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None
    Year: Optional[int] = None
    
    # Water quality parameters (optional, but at least one heavy metal should be present)
    # Basic parameters
    pH: Optional[float] = None
    EC: Optional[float] = None  # µS/cm
    
    # Heavy metals (these are the main focus)
    Fe_ppm: Optional[Any] = None  # Iron in ppm
    As_ppb: Optional[Any] = None  # Arsenic in ppb
    U_ppb: Optional[Any] = None   # Uranium in ppb
    Pb_ppm: Optional[Any] = None  # Lead in ppm
    Cd_ppb: Optional[Any] = None  # Cadmium in ppb
    Cr_ppm: Optional[Any] = None  # Chromium in ppm
    Hg_ppb: Optional[Any] = None  # Mercury in ppb
    
    # Other parameters (optional)
    CO3: Optional[float] = None
    HCO3: Optional[float] = None
    Cl: Optional[float] = None
    F: Optional[float] = None
    SO4: Optional[float] = None
    NO3: Optional[float] = None
    PO4: Optional[float] = None
    Total_Hardness: Optional[float] = None
    Ca: Optional[float] = None
    Mg: Optional[float] = None
    Na: Optional[float] = None
    K: Optional[float] = None

    class Config:
        # Allow extra fields
        extra = "allow"

class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: str
    message: str
    engine_loaded: bool

class EvaluationResponse(BaseModel):
    """Response model for evaluation results."""
    Location: Optional[str]
    State: Optional[str] 
    District: Optional[str]
    Year: Optional[int]
    Coordinates: Optional[Dict[str, Optional[float]]]
    Overall_Risk: str
    Elements_Tested: int
    Results: Dict[str, Any]
    Summary: Optional[Dict[str, Any]] = None

# Add a response model for root endpoint
class RootResponse(BaseModel):
    message: str
    version: str
    endpoints: Dict[str, str]

# API Endpoints

@app.get("/", response_model=RootResponse)
async def root():
    """Root endpoint with API information."""
    return RootResponse(
        message="Health Impact Engine API",
        version="1.0.0",
        endpoints={
            "health_check": "GET /health-check",
            "evaluate": "POST /evaluate",
            "docs": "GET /docs"
        }
    )

@app.get("/health-check", response_model=HealthCheckResponse)
async def health_check():
    """Check if the API and engine are working properly."""
    return HealthCheckResponse(
        status="ok",
        message="Health Impact Engine API is running",
        engine_loaded=engine is not None
    )

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_water_sample(sample: WaterSampleInput):
    """
    Evaluate health risks from a water sample.
    
    Input: Water sample data with heavy metal concentrations
    Output: Risk assessment with diseases, health effects, and symptoms
    """
    if engine is None:
        raise HTTPException(
            status_code=500, 
            detail="Health Impact Engine is not properly initialized"
        )
    
    try:
        # Convert Pydantic model to dictionary
        sample_dict = sample.dict(exclude_none=True)
        
        # Map field names to match engine expectations
        field_mapping = {
            'Fe_ppm': 'Fe (ppm)',
            'As_ppb': 'As (ppb)', 
            'U_ppb': 'U (ppb)',
            'Pb_ppm': 'Pb (ppm)',
            'Cd_ppb': 'Cd (ppb)',
            'Cr_ppm': 'Cr (ppm)',
            'Hg_ppb': 'Hg (ppb)'
        }
        
        # Rename fields to match engine expectations
        for api_field, engine_field in field_mapping.items():
            if api_field in sample_dict:
                sample_dict[engine_field] = sample_dict.pop(api_field)
        
        # Evaluate the sample
        results = engine.evaluate_sample(sample_dict)
        
        # Add summary statistics
        summary = engine.get_summary_statistics(results)
        results['Summary'] = summary
        
        logger.info(f"Successfully evaluated sample for location: {results.get('Location', 'Unknown')}")
        
        return EvaluationResponse(**results)
        
    except Exception as e:
        logger.error(f"Error evaluating sample: {e}")
        raise HTTPException(status_code=500, detail=f"Error evaluating sample: {str(e)}")

@app.get("/rules")
async def get_rules():
    """Get the current health rules (for debugging/reference)."""
    if engine is None:
        raise HTTPException(
            status_code=500,
            detail="Health Impact Engine is not properly initialized"
        )
    
    return engine.rules

@app.get("/elements")
async def get_supported_elements():
    """Get list of supported heavy metals."""
    if engine is None:
        raise HTTPException(
            status_code=500,
            detail="Health Impact Engine is not properly initialized"
        )
    
    if 'heavy_metals' not in engine.rules:
        return {"elements": []}
    
    elements = []
    for element, data in engine.rules['heavy_metals'].items():
        elements.append({
            'element': element,
            'name': data.get('name', element),
            'unit': data.get('unit', 'mg/L'),
            'permissible_limit': data.get('permissible_limit')
        })
    
    return {"elements": elements}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "message": "Check /docs for available endpoints"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "message": "Please check the logs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)