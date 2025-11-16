from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.database.schemas import RecognitionLogCreate
from app.services.recognition_log_service import (
    create_recognition_log_service,
    get_all_recognition_logs_service,
    get_recognition_log_by_id_service,
    get_recognition_logs_by_student_service,
    get_recognition_logs_by_session_service,
    delete_recognition_log_service
)

router = APIRouter(prefix="/recognition-logs", tags=["Recognition Logs"])


@router.post("/")
async def create_log(payload: RecognitionLogCreate):
    # accept a subset of fields; service will set event_time if missing
    return await create_recognition_log_service(payload.dict(exclude_none=True))


@router.get("/")
async def list_logs(limit: int = Query(100, ge=1, le=1000)):
    return await get_all_recognition_logs_service(limit=limit)


@router.get("/{log_id}")
async def get_log(log_id: str):
    return await get_recognition_log_by_id_service(log_id)


@router.get("/student/{student_id}")
async def get_logs_by_student(student_id: str, limit: int = Query(100, ge=1, le=1000)):
    return await get_recognition_logs_by_student_service(student_id, limit=limit)


@router.get("/session/{session_id}")
async def get_logs_by_session(session_id: str, limit: int = Query(100, ge=1, le=1000)):
    return await get_recognition_logs_by_session_service(session_id, limit=limit)


@router.delete("/{log_id}")
async def delete_log(log_id: str):
    return await delete_recognition_log_service(log_id)
