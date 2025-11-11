from fastapi import APIRouter, HTTPException
from app.database.schemas import StudentBase
from app.services.student_service import (
    add_student_service,
    get_all_students_service,
    get_student_by_id_service,
    delete_student_service,
)

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/")
async def add_student(student: StudentBase):
    return await add_student_service(student.dict())

@router.get("/")
async def get_students():
    return await get_all_students_service()

@router.get("/{student_id}")
async def get_student(student_id: str):
    student = await get_student_by_id_service(student_id)
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")

@router.delete("/{student_id}")
async def delete_student(student_id: str):
    deleted = await delete_student_service(student_id)
    if deleted:
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Student not found")
