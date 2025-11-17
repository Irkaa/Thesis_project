from bson import ObjectId
from app.database.connection import db

student_embeddings = db["student_embeddings"]
students = db["students"]


async def add_student_embedding_service(student_id: str, embedding: list[float]):
    # Check if student exists
    try:
        obj_id = ObjectId(student_id)
    except:
        return None  # invalid ObjectId

    student = await students.find_one({"_id": obj_id})
    if not student:
        return None  # student not found

    # Remove old embedding if exists
    await student_embeddings.delete_many({"student_id": student_id})

    # Insert new embedding
    doc = {
        "student_id": student_id,
        "embedding": embedding
    }

    result = await student_embeddings.insert_one(doc)

    return {
        "id": str(result.inserted_id),
        "student_id": student_id,
        "embedding_length": len(embedding)
    }
