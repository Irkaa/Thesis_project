from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from app.services.recognition_service import recognize_multiple_images_service
from app.services.attendance_service import mark_attendance_from_recognition

router = APIRouter(prefix="/recognition", tags=["Recognition"])


@router.post("/take-attendance")
async def take_attendance(
    class_session_id: str = Form(...),
    images: List[UploadFile] = File(...)
):
    """
    Upload multiple images → detect students → mark attendance for a class session.
    """

    if len(images) == 0:
        raise HTTPException(status_code=400, detail="At least one image is required.")

    # Read image bytes
    image_bytes_list = []
    for img in images:
        image_bytes_list.append(await img.read())

    # Step 1: Run recognition across all images
    try:
        detected = await recognize_multiple_images_service(image_bytes_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recognition failed: {str(e)}")

    # Extract student IDs from recognition results
    detected_ids = [item["student_id"] for item in detected]

    # Step 2: Mark attendance based on detected IDs
    try:
        attendance_result = await mark_attendance_from_recognition(
            class_session_id,
            detected_ids
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Attendance update failed: {str(e)}")

    return {
        "detected_students": detected,
        "attendance_summary": attendance_result
    }
