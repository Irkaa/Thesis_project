from bson import ObjectId
from datetime import datetime
from pymongo import ReturnDocument
from app.database.connection import class_collection, student_collection


def class_helper(c):
    return {
        "id": str(c["_id"]),
        "class_name": c["class_name"],
        "teacher_id": c["teacher_id"],
        "student_ids": c.get("student_ids", []),
        "created_at": c.get("created_at")
    }


async def create_class_service(class_name: str, teacher_id: str):
    doc = {
        "class_name": class_name,
        "teacher_id": teacher_id,
        "student_ids": [],
        "created_at": datetime.utcnow()
    }
    result = await class_collection.insert_one(doc)
    new_class = await class_collection.find_one({"_id": result.inserted_id})
    return class_helper(new_class)


async def get_all_classes_service(skip: int = 0, limit: int = 100):
    """Added pagination"""
    res = []
    cursor = class_collection.find().skip(skip).limit(limit)
    async for c in cursor:
        res.append(class_helper(c))
    return res


async def add_student_to_class_service(class_id: str, student_id: str):
    """Optimized: removed redundant query"""
    # Validate ObjectId format
    if not ObjectId.is_valid(class_id):
        return None, "Invalid class_id format"
    if not ObjectId.is_valid(student_id):
        return None, "Invalid student_id format"
    
    # Check class exists
    class_obj = await class_collection.find_one({"_id": ObjectId(class_id)})
    if not class_obj:
        return None, "Class not found"
    
    # Check student exists
    student = await student_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        return None, "Student not found"
    
    # Update and return in one operation (OPTIMIZED!)
    updated = await class_collection.find_one_and_update(
        {"_id": ObjectId(class_id)},
        {"$addToSet": {"student_ids": student_id}},
        return_document=ReturnDocument.AFTER
    )
    
    return class_helper(updated), None