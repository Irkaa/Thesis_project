from app.database.connection import db
from app.database.models import student_helper
from bson import ObjectId

student_collection = db["students"]

async def add_student_service(student_data: dict):
    result = await student_collection.insert_one(student_data)
    return {"id": str(result.inserted_id), **student_data}

async def get_all_students_service():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students

async def get_student_by_id_service(student_id: str):
    student = await student_collection.find_one({"student_id": ObjectId(student_id)})
    return student_helper(student) if student else None

async def delete_student_service(student_id: str):
    result = await student_collection.delete_one({"student_id": ObjectId(student_id)})
    return result.deleted_count == 1
