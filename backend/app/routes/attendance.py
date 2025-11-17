from fastapi import APIRouter, HTTPException, Depends
from app.services.attendance_service import (
    mark_attendance_service,
    get_attendance_by_student_service,
    get_attendance_by_session_service,
)
from app.utils.auth_dependency import get_current_user
from app.utils.rbac import RoleChecker

router = APIRouter(prefix="/attendance", tags=["Attendance"])

# RBAC dependencies
TeacherOrAdmin = RoleChecker(["teacher", "admin"])
AdminOnly = RoleChecker(["admin"])


# ---------------------------------------------------------
# 1. MANUAL ATTENDANCE OVERRIDE (TEACHER OR ADMIN)
# ---------------------------------------------------------
@router.post("/{student_id}", dependencies=[Depends(TeacherOrAdmin)])
async def mark_attendance_manual(
    student_id: str,
    status: str,
    session_id: str,
    user=Depends(get_current_user)
):
    """
    Manual override by teacher/admin.
    Corrects or sets attendance manually.
    """
    try:
        result = await mark_attendance_service(
            student_id=student_id,
            session_id=session_id,
            status=status,
            recognized_confidence=None  # manual entry
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# 2. GET ATTENDANCE FOR A SINGLE STUDENT
# ---------------------------------------------------------
@router.get("/student/{student_id}", dependencies=[Depends(TeacherOrAdmin)])
async def get_student_attendance(student_id: str):
    return await get_attendance_by_student_service(student_id)


# ---------------------------------------------------------
# 3. GET ATTENDANCE FOR A SESSION
# ---------------------------------------------------------
@router.get("/session/{session_id}", dependencies=[Depends(TeacherOrAdmin)])
async def get_session_attendance(session_id: str):
    return await get_attendance_by_session_service(session_id)
