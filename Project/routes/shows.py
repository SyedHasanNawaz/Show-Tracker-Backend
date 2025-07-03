"""
shows.py

This file defines the API endpoints related to TV show management for the Tracker API application.

How it works:
- Uses FastAPI's APIRouter to group all show-related endpoints together.
- Imports the shows_db collection from the database module to interact with show data in MongoDB.
- Imports the Show model from the models module to validate and structure show data.
- Provides endpoints for adding new shows, listing all shows, and retrieving details for a specific show.

Key Concepts:
- Endpoints use Pydantic models to validate incoming data and structure responses.
- All show data is stored and retrieved from the MongoDB collection.
- Endpoints are grouped using a router for better organization and modularity.

Other modules can import this router to include show-related endpoints in the main FastAPI app.
"""

from fastapi import APIRouter, HTTPException
from database import shows_db
from models import Show

# Creating a router for show-related endpoints.
router = APIRouter()

# Endpoint to add a new show.
# Accepts a Show object, stores it in the database, and returns a success message.
@router.post("/shows/add")
def add_show(show: Show):
    shows_db.insert_one(show.dict())
    return {"message": "Show added successfully"}

# Endpoint to list all shows.
# Retrieves all shows from the database and returns them as a list.
@router.get("/shows")
def list_shows():
    shows = list(shows_db.find({}, {"_id": 0}))
    return {"shows": shows}

# Endpoint to get details of a specific show by its ID.
# Returns show details if found, otherwise raises an error.
@router.get("/shows/{show_id}")
def get_show(show_id: str):
    show = shows_db.find_one({"id": show_id}, {"_id": 0})
    if show:
        return show
    raise HTTPException(status_code=404, detail="Show not found")

# Endpoint to update an existing show's details.
# Accepts a show ID and a Show object with updated data.
# Returns a success message if the show is updated, otherwise raises an error.
@router.put("/shows/{show_id}")
def update_show(show_id: str, updated_show: Show):
    result = shows_db.update_one({"id": show_id}, {"$set": updated_show.dict()})
    if result.modified_count:
        return {"message": "Show updated successfully"}
    raise HTTPException(status_code=404, detail="Show not found")

# Endpoint to delete a show by its ID.
# Removes the show from the database and returns a success message.
@router.delete("/shows/{show_id}")
def delete_show(show_id: str):
    result = shows_db.delete_one({"id": show_id})
    if result.deleted_count:
        return {"message": "Show deleted successfully"}
    raise HTTPException(status_code=404, detail="Show not found")
