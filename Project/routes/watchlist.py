"""
watchlist.py

This file defines the API endpoints related to managing user watchlists for the Tracker API application.

How it works:
- Uses FastAPI's APIRouter to group all watchlist-related endpoints together.
- Imports the watchlist_db collection from the database module to interact with watchlist data in MongoDB.
- Imports the Watchlist model from the models module to validate and structure watchlist data.
- Uses authentication to ensure users can only modify their own watchlists.
- Provides endpoints for adding shows to a user's watchlist, listing all watchlist items for a user, updating watchlist entries, and removing shows from the watchlist.

Key Concepts:
- Endpoints use Pydantic models to validate incoming data and structure responses.
- All watchlist data is stored and retrieved from the MongoDB collection.
- Endpoints are grouped using a router for better organization and modularity.
- Only authenticated users can add, update, or remove shows from their own watchlist.
- Allows users to track which shows they want to watch and manage their watchlist.

Other modules can import this router to include watchlist-related endpoints in the main FastAPI app.
"""

from fastapi import APIRouter, Depends, HTTPException

from auth import get_logged_in_user
from database import watchlist_db
from models import Watchlist

# Creating a router for watchlist-related endpoints.
router = APIRouter()

# Endpoint to add a show to the user's watchlist.
# Accepts a Watchlist object and stores it in the database.
# Only allows if the user is authenticated.
@router.post("/watchlist/add")
def add_to_watchlist(watchlist: Watchlist, user_id: str = Depends(get_logged_in_user)):
    if watchlist_db.find_one({"id": watchlist.id, "user_id": user_id}):
        return {"Error": "Show already in watchlist"}
    watchlist_db.insert_one({**watchlist.dict(), "user_id": user_id})
    return {"Message": "Show added to watchlist"}

# Endpoint to list all watchlist items for a specific user.
# Returns a list of watchlist entries for the given user_id.
@router.get("/watchlist/{user_id}")
def list_watchlist(user_id: str):
    items = list(watchlist_db.find({"user_id": user_id}, {"_id": 0}))
    return {"watchlist": items}

# Endpoint to update a watchlist entry.
# Accepts a watchlist_id and an updated Watchlist object, updates the entry if found and owned by the user.
@router.put("/watchlist/{watchlist_id}")
def update_watchlist(watchlist_id: str, updated: Watchlist, user_id: str = Depends(get_logged_in_user)):
    if not watchlist_db.find_one({"id": watchlist_id, "user_id": user_id}):
        return {"Error": "Unauthorized access to watchlist"}
    watchlist_db.update_one({"id": watchlist_id}, {"$set": updated.dict()})
    return {"Message": "Watchlist entry updated"}

# Endpoint to remove a show from the user's watchlist.
# Accepts a watchlist_id and deletes the entry if found and owned by the user.
@router.delete("/watchlist/{watchlist_id}")
def remove_from_watchlist(watchlist_id: str, user_id: str = Depends(get_logged_in_user)):
    if not watchlist_db.find_one({"id": watchlist_id, "user_id": user_id}):
        return {"Error": "Unauthorized access to watchlist"}
    result = watchlist_db.delete_one({"id": watchlist_id})
    if result.deleted_count == 1:
        return {"Message": "Show removed from watchlist"}
    raise HTTPException(status_code=404, detail="Watchlist entry not found")
