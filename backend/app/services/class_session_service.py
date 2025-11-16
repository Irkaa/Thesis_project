from bson import ObjectId
from app.database.connection import db
from app.database.models import class_session_helper

session_collection = db["class_sessions"]
class_collection = db["classes"]


async def create_class_session_service(data: dict):
    # validate class exists
    class_id = data["class_id"]
    if not ObjectId.is_valid(class_id):
        return None

    cls = await class_collection.find_one({"_id": ObjectId(class_id)})
    if not cls:
        return "CLASS_NOT_FOUND"

    result = await session_collection.insert_one(data)
    created = await session_collection.find_one({"_id": result.inserted_id})
    return class_session_helper(created)


async def get_all_sessions_service():
    sessions = []
    async for sess in session_collection.find():
        sessions.append(class_session_helper(sess))
    return sessions


async def get_session_by_id_service(session_id: str):
    if not ObjectId.is_valid(session_id):
        return None

    sess = await session_collection.find_one({"_id": ObjectId(session_id)})
    return class_session_helper(sess) if sess else None


async def update_session_service(session_id: str, data: dict):
    if not ObjectId.is_valid(session_id):
        return None

    # if updating class_id, validate
    if "class_id" in data:
        if not ObjectId.is_valid(data["class_id"]):
            return "INVALID_CLASS_ID"
        cls = await class_collection.find_one({"_id": ObjectId(data["class_id"])})
        if not cls:
            return "CLASS_NOT_FOUND"

    await session_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": data}
    )

    updated = await session_collection.find_one({"_id": ObjectId(session_id)})
    return class_session_helper(updated) if updated else None


async def delete_session_service(session_id: str):
    if not ObjectId.is_valid(session_id):
        return False

    result = await session_collection.delete_one({"_id": ObjectId(session_id)})
    return result.deleted_count == 1
