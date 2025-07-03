"""
main.py

This file is the entry point for the Tracker API application. It uses FastAPI, a modern web framework for building APIs with Python.

How it works:
- Imports FastAPI and creates an app instance.
- Imports routers from different modules, each handling a specific part of the application (users, shows, episodes, watchlist, watched).
- Includes these routers in the main FastAPI app, making all their endpoints available in the API.
- Defines a root endpoint ("/") that returns a simple welcome message when accessed.
- When you run this file, FastAPI starts a web server that listens for HTTP requests and routes them to the correct function based on the URL.

Key Concepts:
- Routers help organize the code by grouping related endpoints together (for example, all user-related endpoints are in the users router).
- The root endpoint ("/") acts as a home page or health check for the API.

Other modules can add more endpoints or features by creating new routers and including them in this file.
"""

# Importing FastAPI, a modern web framework for building APIs with Python
from fastapi import FastAPI

# Importing routers (collections of API endpoints) from different modules.
# Each router handles a specific part of the application (users, shows, etc.)
from routes import users, shows, episodes, watchlist, watched

# Creating an instance of the FastAPI application.
# This 'app' object will be used to define routes and start the server.
app = FastAPI()

# Including the routers into the main FastAPI app.
# This means all the endpoints defined in these routers will be available in the API.
# For example, if users.router defines a '/users' endpoint, it will be accessible.
app.include_router(users.router)      # Handles user-related endpoints (e.g., registration, login)
app.include_router(shows.router)      # Handles TV show-related endpoints (e.g., list shows)
app.include_router(episodes.router)   # Handles episode-related endpoints (e.g., list episodes)
app.include_router(watchlist.router)  # Handles user's watchlist endpoints (e.g., add/remove shows)
app.include_router(watched.router)    # Handles endpoints for marking shows/episodes as watched

# Defining the root endpoint ("/").
# When someone visits the base URL of the API (e.g., http://localhost:8000/), this function runs.
@app.get("/")
def root():
    # Returns a simple JSON response with a message.
    # This acts as a home page or a health check for the API.
    return {"message": "Home Page Hai Yeh"}

# How this file works:
# - When you run this file, FastAPI starts a web server.
# - The server listens for HTTP requests and routes them to the correct function based on the URL.
# - The routers organize the code, so each feature (users, shows, etc.) is in its own file.
# - The root endpoint ("/") just returns a welcome message.
