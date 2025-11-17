from fastapi import APIRouter, HTTPException, Depends
from app.services.class_service import (
    create_class_service,
    get_all_classes_service,
    add_student_to_class_service
)
from app.utils.auth_dependency import get_current_user  # FIXED: was jwt_handler
from app.utils.rbac import RoleChecker

router = APIRouter(prefix="/classes", tags=["Classes"])
AdminOnly = RoleChecker(["admin"])


@router.post("/", dependencies=[Depends(AdminOnly)])
async def create_class(data: dict):
    """Create new class - Admin only"""
    class_name = data.get("class_name")
    teacher_id = data.get("teacher_id")

    if not class_name or not teacher_id:
        raise HTTPException(status_code=400, detail="class_name and teacher_id are required")

    result = await create_class_service(class_name, teacher_id)
    return result


@router.get("/", dependencies=[Depends(AdminOnly)])
async def get_classes():
    """Get all classes - Admin only"""
    return await get_all_classes_service()


@router.post("/{class_id}/add-student/{student_id}", dependencies=[Depends(AdminOnly)])
async def add_student(class_id: str, student_id: str):
    """Add student to class - Admin only"""
    updated, error = await add_student_to_class_service(class_id, student_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return updated