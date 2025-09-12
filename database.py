from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")


# Create a single, reusable AsyncIOMotorClient instance
client = AsyncIOMotorClient(MONGO_URI)

# Get the database and collection (async)
db = client.ChemistryDB
element_collection = db.get_collection("elements")
print("✅ Async database connection established.")

# Helper function to serialize MongoDB documents
def element_helper(element) -> dict:
    return {
        "id": str(element["_id"]),
        "element": element["element"],
        "reactions_with_heavy_metals": element["reactions_with_heavy_metals"],
        "reactions_with_environment": element["reactions_with_environment"],
        "compounds_found": element["compounds_found"],
    }