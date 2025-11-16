from bson import ObjectId
from app.database.connection import db
from app.database.models import class_helper

class_collection = db["classes"]


async def create_class_service(data: dict):
    result = await class_collection.insert_one(data)
    created = await class_collection.find_one({"_id": result.inserted_id})
    return class_helper(created)


async def get_all_classes_service():
    classes = []
    async for cls in class_collection.find():
        classes.append(class_helper(cls))
    return classes


async def get_class_by_id_service(class_id: str):
    if not ObjectId.is_valid(class_id):
        return None
    cls = await class_collection.find_one({"_id": ObjectId(class_id)})
    return class_helper(cls) if cls else None


async def update_class_service(class_id: str, data: dict):
    if not ObjectId.is_valid(class_id):
        return None
    await class_collection.update_one(
        {"_id": ObjectId(class_id)},
        {"$set": data}
    )
    updated = await class_collection.find_one({"_id": ObjectId(class_id)})
    return class_helper(updated) if updated else None


async def delete_class_service(class_id: str):
    if not ObjectId.is_valid(class_id):
        return False
    result = await class_collection.delete_one({"_id": ObjectId(class_id)})
    return result.deleted_count == 1
