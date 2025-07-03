"""
models.py

This file defines the data models (schemas) used by the Tracker API application.
It uses Pydantic, a library that helps validate and serialize data for FastAPI.

How it works:
- Each class represents a type of data used in the application (User, Show, Episode, Watchlist, WatchedEpisode).
- These models define the structure and data types for requests and responses in the API.
- FastAPI uses these models to automatically validate incoming data and generate documentation.

Key Concepts:
- All models inherit from Pydantic's BaseModel, which provides validation and serialization.
- The field names and types must match the data stored in the database or sent/received by the API.
- These models are used in route functions to define what data is expected or returned.

Other modules can import these models to use as request bodies, response models, or for data validation.
"""

from pydantic import BaseModel

# Pydantic Models

class User(BaseModel):
    id: str                  # Unique identifier for the user
    username: str            # User's chosen username
    email: str               # User's email address
    password: str            # User's hashed password

class Show(BaseModel):
    id: str                  # Unique identifier for the show
    title: str               # Title of the show
    description: str         # Description of the show
    genre: str               # Genre of the show (e.g., Drama, Comedy)
    release_year: int        # Year the show was released
    type: str                # Type of show (e.g., Series, Movie)

class Episode(BaseModel):
    id: str                  # Unique identifier for the episode
    show_id: str             # ID of the show this episode belongs to
    season_number: int       # Season number
    episode_number: int      # Episode number within the season
    title: str               # Title of the episode
    duration_minutes: int    # Duration of the episode in minutes

class Watchlist(BaseModel):
    id: str                  # Unique identifier for the watchlist entry
    user_id: str             # ID of the user who owns this watchlist
    show_id: str             # ID of the show in the watchlist
    status: str              # Status (e.g., "watching", "completed")
    rating: int              # User's rating for the show
    notes: str               # Any notes the user added

class WatchedEpisode(BaseModel):
    id: str                  # Unique identifier for the watched episode entry
    watchlist_id: str        # ID of the related watchlist entry
    episode_id: str          # ID of the episode that was watched
    watched_at: int          # Timestamp (e.g., Unix time) when the episode was
