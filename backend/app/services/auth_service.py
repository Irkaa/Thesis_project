from bson import ObjectId
from fastapi import HTTPException
from app.database.connection import db
from app.database.models import user_helper
from app.utils.jwt_handler import create_access_token
from passlib.hash import bcrypt

users_collection = db["users"]


async def register_user_service(user_data: dict):
    # Check duplicate email
    exists = await users_collection.find_one({"email": user_data["email"]})
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = bcrypt.hash(user_data["password"])

    user_data["password"] = hashed_pw

    result = await users_collection.insert_one(user_data)
    created = await users_collection.find_one({"_id": result.inserted_id})
    
    return user_helper(created)


async def login_user_service(email: str, password: str):
    user = await users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not bcrypt.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"])})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_helper(user)
    }
