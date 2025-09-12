from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from typing import List

# Import database functions and models
from database import element_collection, element_helper
from models import ElementModel, UpdateElementModel

router = APIRouter()

# POST: Add a new element
@router.post("/", response_description="Add a new element", response_model=ElementModel)
async def create_element(element: ElementModel = Body(...)):
    element_dict = element.dict()
    new_element = await element_collection.insert_one(element_dict)
    created_element = await element_collection.find_one({"_id": new_element.inserted_id})
    return element_helper(created_element)

# GET: Retrieve all elements
@router.get("/", response_description="List all elements", response_model=List[ElementModel])
async def list_elements():
    elements = []
    async for element in element_collection.find():
        elements.append(element_helper(element))
    return elements

# GET: Retrieve a single element by its name
@router.get("/{name}", response_description="Get a single element by name", response_model=ElementModel)
async def show_element(name: str):
    element = await element_collection.find_one({"element": name})
    if element:
        return element_helper(element)
    raise HTTPException(status_code=404, detail=f"Element {name} not found")

# PUT: Update an existing element
@router.put("/{name}", response_description="Update an element", response_model=ElementModel)
async def update_element(name: str, element: UpdateElementModel = Body(...)):
    # Create a dictionary of fields to update, excluding any unset (None) values
    update_data = {k: v for k, v in element.dict().items() if v is not None}

    if len(update_data) >= 1:
        update_result = await element_collection.update_one(
            {"element": name}, {"$set": update_data}
        )

        if update_result.modified_count == 1:
            if (
                updated_element := await element_collection.find_one({"element": name})
            ) is not None:
                return element_helper(updated_element)

    if (
        existing_element := await element_collection.find_one({"element": name})
    ) is not None:
        return element_helper(existing_element)

    raise HTTPException(status_code=404, detail=f"Element {name} not found")

# DELETE: Delete an element
@router.delete("/{name}", response_description="Delete an element")
async def delete_element(name: str):
    delete_result = await element_collection.delete_one({"element": name})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Element {name} not found")