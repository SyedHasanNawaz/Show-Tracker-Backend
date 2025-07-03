"""
episodes.py

This file defines the API endpoints related to episode management for the Tracker API application.

How it works:
- Uses FastAPI's APIRouter to group all episode-related endpoints together.
- Imports the episodes_db and shows_db collections from the database module to interact with episode and show data in MongoDB.
- Imports the Episode model from the models module to validate and structure episode data.
- Provides endpoints for adding, listing, updating, and deleting episodes, as well as listing episodes for a specific show.

Key Concepts:
- Endpoints use Pydantic models to validate incoming data and structure responses.
- All episode data is stored and retrieved from the MongoDB collection.
- Endpoints are grouped using a router for better organization and modularity.
- Includes logic to ensure episodes are only added to valid shows and only lists episodes for series-type shows.

Other modules can import this router to include episode-related endpoints in the main FastAPI app."""

from fastapi import APIRouter

from database import shows_db, episodes_db
from models import Episode

# Creating a router for episode-related endpoints.
router = APIRouter()


# ____________________________________Episodes__________________________

# Endpoint to get all episodes.
# Returns a list of all episodes in the database.
@router.get("/episodes")
def get_episode() :
	return list(episodes_db.find({}, {"_id" : 0}))


# Endpoint to add an episode to a specific show.
# Accepts an Episode object and show_id, adds the episode if the show exists.
@router.post("/shows/{show_id}/episodes")
def add_episodes(episode: Episode, show_id: str) :
	key = show_id
	if shows_db.find_one({"id" : key}) :
		episodes_db.insert_one({
			"id" : episode.id,
			"show_id" : episode.show_id,
			"season_number" : episode.season_number,
			"episode_number" : episode.episode_number,
			"title" : episode.title,
			"duration_minutes" : episode.duration_minutes,
		})
		return {"Message" : "Episode added successfully"}
	return {"Error" : "Episode not added"}


# Endpoint to get a list of episodes for a specific show.
# Only works if the show exists and is of type "Series".
@router.get("/shows/{show_id}/episodes")
def get_list(show_id: str) :
	if not shows_db.find_one({"id" : show_id}) :
		return {"Error" : "Show not found"}
	
	show = shows_db.find_one({"id" : show_id})
	if not show:
		return {"Error" : "Show not found"}
	if show["type"] != "Series" :
		return {"Error" : "Not a series"}
	
	result = []
	for ep in episodes_db.find({"show_id" : show_id}, {"_id" : 0}) :
		result.append(ep)
	if result :
		return {"Episodes" : result}
	
	return {"Error" : "Episodes not found"}


# Endpoint to update an episode's details.
# Accepts an episode_id and an updated Episode object, updates the episode if found.
@router.put("/episodes/{episode_id}")
def update_episode(episode_id: str, updated: Episode) :
	if episodes_db.find_one({"id" : episode_id}) :
		episodes_db.update_one({"id" : episode_id}, {"$set" : {
			"id" : updated.id,
			"show_id" : updated.show_id,
			"season_number" : updated.season_number,
			"episode_number" : updated.episode_number,
			"title" : updated.title,
			"duration_minutes" : updated.duration_minutes
		}})
		return {"Message" : "Episode updated successfully"}
	return {"Error" : "Episode not found"}


# Endpoint to delete an episode.
# Accepts an episode_id, deletes the episode if found.
@router.delete("/episodes/{episode_id}")
def delete_episode(episode_id: str) :
	if episodes_db.find_one({"id" : episode_id}) :
		episodes_db.delete_one({"id" : episode_id})
		return {"Message" : "Episode deleted successfully"}
	return {"Error" : "Episode not found"}
