"""
watched.py

This file defines the API endpoints related to tracking watched episodes for the Tracker API application.

How it works:
- Uses FastAPI's APIRouter to group all watched-episode-related endpoints together.
- Imports the watched_episodes_db and watchlist_db collections from the database module to interact with watched episode and watchlist data in MongoDB.
- Imports the WatchedEpisode model from the models module to validate and structure watched episode data.
- Uses authentication to ensure users can only modify their own watched episodes.
- Provides endpoints for marking episodes as watched, listing all watched episodes for a user, and removing watched records.

Key Concepts:
- Endpoints use Pydantic models to validate incoming data and structure responses.
- All watched episode data is stored and retrieved from the MongoDB collection.
- Endpoints are grouped using a router for better organization and modularity.
- Only authenticated users can add or remove watched episodes from their own watchlist.
- Allows users to track which episodes they have watched and manage their watched history.

Other modules can import this router to include watched-episode-related endpoints in the main FastAPI app.
"""

from fastapi import APIRouter, Depends, HTTPException

from auth import get_logged_in_user
from database import watchlist_db, watched_episodes_db
from models import WatchedEpisode

# Creating a router for watched-episode-related endpoints.
router = APIRouter()


# Endpoint to mark an episode as watched.
# Accepts a WatchedEpisode object and stores it in the database.
# Only allows if the user owns the watchlist.
@router.post("/watched/add")
def add_watched_episode(watched: WatchedEpisode, user_id: str = Depends(get_logged_in_user)):
    if not watchlist_db.find_one({"id": watched.watchlist_id, "user_id": user_id}):
        return {"Error": "Unauthorized access to watchlist"}
    watched_episodes_db.insert_one(watched.dict())
    return {"Message": "Added to Watched Episodes of User successfully"}


# Endpoint to list all watched episodes for a specific user.
# Returns a list of watched episodes for the given user_id.
@router.get("/watched/{user_id}")
def list_watched_episodes(user_id: str):
    watched = list(watched_episodes_db.find({"user_id": user_id}, {"_id": 0}))
    return {"watched_episodes": watched}


# Endpoint to remove a watched episode record.
# Accepts a watched episode ID and deletes the record if found.
# Only allows if the user owns the watchlist.
@router.delete("/watched/{watched_id}/{watchlist_id}")
def remove_watched_episode(watched_id: str, watchlist_id: str, user_id: str = Depends(get_logged_in_user)):
    if not watchlist_db.find_one({"id": watchlist_id, "user_id": user_id}):
        return {"Error": "Unauthorized access to watchlist"}
    result = watched_episodes_db.delete_one({"id": watched_id})
    if result.deleted_count == 1:
        return {"message": "Watched episode removed"}
    raise HTTPException(status_code=404, detail="Watched Episode not found")
