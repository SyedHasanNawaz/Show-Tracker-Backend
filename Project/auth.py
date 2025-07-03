"""
auth.py

This file handles authentication and password security for the Tracker API application.

How it works:
- Uses JWT (JSON Web Tokens) to securely manage user authentication.
- Provides functions to hash passwords, verify passwords, create JWT tokens, and extract the logged-in user from a token.
- Uses FastAPI's OAuth2PasswordBearer for extracting tokens from requests.
- Uses passlib for secure password hashing.

Key Concepts:
- JWT tokens are used to identify users after they log in, so they don't have to send their password with every request.
- Passwords are never stored in plain text; they are hashed before saving to the database.
- The `get_logged_in_user` function is used as a dependency in routes to ensure the user is authenticated.

Other modules can import these functions to handle authentication and password security.
"""
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

# ___________________________________JWT Token________________________

load_dotenv()
# Secret key for encoding and decoding JWT tokens.
SECRET_KEY = os.getenv("SECRET_KEY", "Hasan1234567890")
# Algorithm used for JWT encoding.
ALGORITHM = os.getenv("ALGORITHM", "HS256")
# Token expiration time in minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# OAuth2 scheme for extracting the token from the Authorization header.
token_extractor = OAuth2PasswordBearer(tokenUrl="/users/login")

# Password hashing context using bcrypt algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to hash a plain password before storing it in the database.
def hash_password(password: str):
    return pwd_context.hash(password)


# Function to verify a plain password against its hashed version.
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# Function to create a JWT token for a user.
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token


# Dependency function to get the currently logged-in user from the JWT token.
def get_logged_in_user(token: str = Depends(token_extractor)):
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # 'sub' holds the user ID

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token (no user)")

        return user_id

    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Token is invalid or expired") from exc
