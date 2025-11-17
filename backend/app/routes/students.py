from fastapi import APIRouter, HTTPException, Depends
from app.database.schemas import StudentBase
from app.services.student_service import (
    add_student_service,
    get_all_students_service,
    get_student_by_id_service,
    delete_student_service,
)
from app.utils.auth_dependency import get_current_user
from app.utils.rbac import AdminOnly, TeacherOrAdmin

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", dependencies=[Depends(AdminOnly)])
async def add_student(student: StudentBase):
    """Create new student - Admin only"""
    return await add_student_service(student.dict())


@router.get("/", dependencies=[Depends(TeacherOrAdmin)])
async def get_students():
    """List all students - Teachers and Admins"""
    return await get_all_students_service()


@router.get("/{student_id}", dependencies=[Depends(TeacherOrAdmin)])
async def get_student(student_id: str):
    """Get specific student - Teachers and Admins"""
    student = await get_student_by_id_service(student_id)
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")


@router.delete("/{student_id}", dependencies=[Depends(AdminOnly)])
async def delete_student(student_id: str):
    """Delete student - Admin only"""
    deleted = await delete_student_service(student_id)
    if deleted:
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Student not found")