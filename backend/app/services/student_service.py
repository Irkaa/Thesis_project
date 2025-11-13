from app.database.connection import db
from app.database.models import student_helper
from bson import ObjectId, errors
from fastapi import HTTPException, status

student_collection = db["students"]


# ---------------------------
# Service Layer: Students
# ---------------------------

async def add_student_service(student_data: dict):
    """
    Insert a new student record.
    Prevents duplicate student_id entries.
    """
    try:
        # Check for existing student_id
        existing = await student_collection.find_one({"student_id": student_data["student_id"]})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with ID '{student_data['student_id']}' already exists.",
            )

        result = await student_collection.insert_one(student_data)
        created_student = await student_collection.find_one({"_id": result.inserted_id})
        if not created_student:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create student record."
            )
        return student_helper(created_student)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding student: {str(e)}",
        )


async def get_all_students_service():
    """
    Retrieve all students.
    """
    try:
        students = []
        async for student in student_collection.find():
            students.append(student_helper(student))
        return students
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving students: {str(e)}",
        )


async def get_student_by_id_service(student_id: str):
    """
    Retrieve a student either by ObjectId or by custom student_id.
    """
    try:
        student = None
        # Try Mongo ObjectId first
        try:
            student = await student_collection.find_one({"_id": ObjectId(student_id)})
        except errors.InvalidId:
            # Fall back to custom student_id field
            student = await student_collection.find_one({"student_id": student_id})

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID '{student_id}' not found.",
            )

        return student_helper(student)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving student: {str(e)}",
        )


async def delete_student_service(student_id: str):
    """
    Delete a student by either ObjectId or student_id.
    """
    try:
        result = None
        try:
            result = await student_collection.delete_one({"_id": ObjectId(student_id)})
        except errors.InvalidId:
            result = await student_collection.delete_one({"student_id": student_id})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID '{student_id}' not found or already deleted.",
            )

        return {"status": "deleted", "student_id": student_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting student: {str(e)}",
        )
