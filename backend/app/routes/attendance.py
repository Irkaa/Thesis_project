from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.attendance_service import recognize_and_mark_attendance_service

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/recognize/{session_id}")
async def recognize_and_mark(session_id: str, image: UploadFile = File(...)):
    image_bytes = await image.read()
    return await recognize_and_mark_attendance_service(image_bytes, session_id)
