"""
database.py

This file sets up the connection between the Tracker API application and a MongoDB database.

How it works:
- Connects to a MongoDB server running on your computer (localhost) at the default port 27017.
- Selects (or creates) a database named 'Tracker_API'.
- Defines references to different collections (like tables in SQL) within the database:
    - users_db: Stores user information (usernames, emails, passwords, etc.)
    - shows_db: Stores TV show details (titles, genres, descriptions, etc.)
    - episodes_db: Stores episode details for each show (episode titles, numbers, etc.)
    - watchlist_db: Stores users' watchlists (shows/episodes they want to watch)
    - watched_episodes_db: Stores records of episodes users have already watched

Other modules can import these collection variables to interact with the database.
No data is added or changed here; this file only sets up the connection and references.
"""

# Importing MongoClient from pymongo, which allows Python to connect to a MongoDB database.
from pymongo import MongoClient
import os
from dotenv import load_dotenv
# _____________________________________Mongo DB________________________
# Creating a connection to the MongoDB server running on your own computer (localhost) at the default port 27017.

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Create a MongoClient instance using the MONGO_URI environment variable.
client = MongoClient(MONGO_URI)

# Selecting (or creating, if it doesn't exist) a database named 'Tracker_API'.
db = client["Show_Tracker"]

# Creating references to different collections (like tables in SQL) within the 'Tracker_API' database.
# Each collection stores a specific type of data for the application.

users_db = db["users_db"]               # Stores user information (e.g., usernames, emails, passwords)
shows_db = db["shows_db"]               # Stores TV show details (e.g., titles, genres, descriptions)
episodes_db = db["episodes_db"]         # Stores episode details for each show (e.g., episode titles, numbers)
watchlist_db = db["watchlist_db"]       # Stores users' watchlists (shows/episodes they want to watch)
watched_episodes_db = db["watched_episodes_db"]  # Stores records of episodes users have already watched

# How this file works:
# - This file sets up the connection between your Python code and the MongoDB database.
# - It prepares access to different collections, so other parts of your app can easily read/write data.
# - Other modules can import these collection variables (like users_db) to interact with the database.
# - No data is added or changed here; this file only establishes the connection and defines the structure.

