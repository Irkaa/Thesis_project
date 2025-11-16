from bson import ObjectId
from datetime import datetime
from app.database.connection import db
from app.database.models import student_embedding_helper
from fastapi import HTTPException

embedding_collection = db["student_embeddings"]
student_collection = db["students"]


async def add_student_embedding_service(student_id: str, embedding: list, photo_url: str = None):
    # Validate student exists
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student_id")

    student = await student_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    payload = {
        "student_id": student_id,
        "embedding": embedding,
        "photo_s3_url": photo_url,
        "version": 1,
        "created_at": datetime.utcnow(),
    }

    result = await embedding_collection.insert_one(payload)
    created = await embedding_collection.find_one({"_id": result.inserted_id})

    return student_embedding_helper(created)
