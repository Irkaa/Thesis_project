from fastapi import APIRouter, HTTPException, Depends
from app.services.class_session_service import create_class_session_service
from app.utils.rbac import TeacherOrAdmin

router = APIRouter(prefix="/class-sessions", tags=["Class Sessions"])


@router.post("/{class_id}", dependencies=[Depends(TeacherOrAdmin)])
async def create_session(class_id: str):
    """Create new class session - Teachers and Admins"""
    session, error = await create_class_session_service(class_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return session