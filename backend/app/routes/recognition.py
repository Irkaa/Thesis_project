from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List
from app.services.recognition_service import recognize_multiple_images
from app.services.attendance_service import mark_attendance_from_recognition
from app.utils.auth_dependency import get_current_user

router = APIRouter(prefix="/recognition", tags=["Recognition"])


@router.post("/take-attendance")
async def take_attendance(
    class_session_id: str = Form(...),
    images: List[UploadFile] = File(...),
    user = Depends(get_current_user)
):
    """
    Upload multiple group photos → recognize → mark attendance.
    """

    if len(images) == 0:
        raise HTTPException(status_code=400, detail="At least one image is required.")

    image_bytes_list = [await img.read() for img in images]

    try:
        result = await recognize_multiple_images(image_bytes_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recognition failed: {str(e)}")

    # Extract detected student IDs from result
    detected_ids = result["detected_students"]

    try:
        attendance_result = await mark_attendance_from_recognition(
            class_session_id,
            detected_ids
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Attendance update failed: {str(e)}")

    return {
        "detected_students": detected_ids,
        "all_detections": result["all_detections"],
        "vote_counts": result["vote_counts"],
        "attendance_summary": attendance_result
    }
