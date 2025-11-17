from fastapi import APIRouter, HTTPException, Depends
from app.services.recognition_log_service import (
    get_all_logs_service,
    get_logs_for_class_service,
    get_logs_for_session_service
)
from app.utils.rbac import TeacherOrAdmin

router = APIRouter(prefix="/recognition-logs", tags=["Recognition Logs"])


@router.get("/", dependencies=[Depends(TeacherOrAdmin)])
async def get_all_logs():
    """Get all recognition logs - Teachers and Admins"""
    return await get_all_logs_service()


@router.get("/class/{class_id}", dependencies=[Depends(TeacherOrAdmin)])
async def get_logs_by_class(class_id: str):
    """Get recognition logs for specific class - Teachers and Admins"""
    return await get_logs_for_class_service(class_id)


@router.get("/session/{session_id}", dependencies=[Depends(TeacherOrAdmin)])
async def get_logs_by_session(session_id: str):
    """Get recognition logs for specific session - Teachers and Admins"""
    return await get_logs_for_session_service(session_id)