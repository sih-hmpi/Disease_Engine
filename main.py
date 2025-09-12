from fastapi import FastAPI
from routes.element import router as element_router

app = FastAPI()

# Include the router from routes/element.py
# All routes in element_router will be prefixed with /api/elements
app.include_router(element_router, tags=["Elements"], prefix="/api/elements")

@app.get("/")
async def root():
    return {"message": "Welcome to the Chemistry API. Navigate to /docs for the API documentation."}

# Input in the GET /api/elements/{name} Show Single Element should be like:
# Arsenic (As)