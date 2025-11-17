from app.database.connection import (
    student_collection,
    student_embedding_collection,
    attendance_collection
)
from app.database.models import student_helper
from bson import ObjectId, errors
from fastapi import HTTPException, status


async def add_student_service(student_data: dict):
    """Insert a new student record"""
    existing = await student_collection.find_one({"student_id": student_data["student_id"]})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with ID '{student_data['student_id']}' already exists."
        )
    
    result = await student_collection.insert_one(student_data)
    created_student = await student_collection.find_one({"_id": result.inserted_id})
    if not created_student:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create student record."
        )
    return student_helper(created_student)


async def get_all_students_service(skip: int = 0, limit: int = 100):
    """Retrieve all students with pagination"""
    students = []
    cursor = student_collection.find().skip(skip).limit(limit)
    async for student in cursor:
        students.append(student_helper(student))
    return students


async def get_student_by_id_service(student_id: str):
    """Retrieve student by ObjectId or custom student_id"""
    student = None
    
    # Try ObjectId first (more efficient)
    if ObjectId.is_valid(student_id):
        student = await student_collection.find_one({"_id": ObjectId(student_id)})
    
    # Fallback to custom student_id
    if not student:
        student = await student_collection.find_one({"student_id": student_id})
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' not found."
        )
    
    return student_helper(student)


async def delete_student_service(student_id: str):
    """
    Delete student with CASCADE delete.
    Also removes embeddings and attendance records.
    """
    # Find student first
    student = None
    if ObjectId.is_valid(student_id):
        student = await student_collection.find_one({"_id": ObjectId(student_id)})
        query = {"_id": ObjectId(student_id)}
    else:
        student = await student_collection.find_one({"student_id": student_id})
        query = {"student_id": student_id}
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' not found."
        )
    
    # CASCADE DELETE
    student_mongo_id = str(student["_id"])
    
    # Delete student embeddings
    await student_embedding_collection.delete_many({"student_id": student_mongo_id})
    
    # Delete attendance records
    await attendance_collection.delete_many({"student_id": student_mongo_id})
    
    # Delete student record
    result = await student_collection.delete_one(query)
    
    return {
        "status": "deleted",
        "student_id": student_id,
        "cascaded": {
            "embeddings_deleted": True,
            "attendance_deleted": True
        }
    }