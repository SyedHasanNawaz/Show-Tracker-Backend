"""
users.py

This file defines the API endpoints related to user registration, login, and authentication for the Tracker API application.

How it works:
- Uses FastAPI's APIRouter to group all user-related endpoints together.
- Imports utility functions for password hashing, verification, and token creation from the auth module.
- Imports the users_db collection from the database module to interact with user data in MongoDB.
- Imports the User model from the models module to validate and structure user data.
- Provides endpoints for user registration, login, and authentication.

Key Concepts:
- Registration endpoint hashes the user's password before storing it and returns a JWT token upon success.
- Login endpoint checks the username and password, and returns a JWT token if credentials are valid.
- Authentication endpoint verifies user credentials and returns a verification message.
- All sensitive operations use hashed passwords and JWT tokens for security.

Other modules can import this router to include user-related endpoints in the main FastAPI app.
"""

from fastapi import APIRouter, Form, HTTPException

from auth import hash_password, verify_password, create_token
from database import users_db
from models import User

# Creating a router for user-related endpoints.
router = APIRouter()

# Endpoint for user registration.
# Accepts a User object, hashes the password, stores the user in the database, and returns a JWT token.
@router.post("/users/register")
def register(user: User):
    users_db.insert_one({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password)
    })
    token = create_token({"sub": user.id})
    return {"message": "Registered", "access_token": token}

# Endpoint for user login.
# Accepts username and password as form data, verifies credentials, and returns a JWT token if valid.
@router.post("/users/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = users_db.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        token = create_token({"sub": user["id"]})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Endpoint for user authentication (verification).
# Accepts a User object, verifies credentials, and returns a verification message.
@router.post("/users/authenticate")
def authenticate(user: User):
    db_user = users_db.find_one({"username": user.username})
    if db_user and verify_password(user.password, db_user["password"]):
        return {"Message": "User Verified"}
    return {"Error": "User Not Verified"}
