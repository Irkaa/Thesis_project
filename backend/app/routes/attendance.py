from fastapi import APIRouter, HTTPException, File, UploadFile
from app.services.attendance_service import (
    mark_attendance_service,
    get_attendance_by_date_service,
    get_student_attendance_history_service,
)
from app.services.recognition_service import recognize_face_service

# define the router first
router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/{student_id}")
async def mark_attendance(student_id: str, status: str):
    """
    Mark a student's attendance manually.
    Status should be 'present' or 'absent'.
    """
    result = await mark_attendance_service(student_id, status)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found or could not be marked.")
    return {"message": "Attendance marked successfully", "data": result}


@router.get("/date/{date}")
async def get_attendance_by_date(date: str):
    """
    Retrieve all attendance records for a specific date.
    """
    records = await get_attendance_by_date_service(date)
    return {"date": date, "records": records}


@router.get("/student/{student_id}")
async def get_student_attendance_history(student_id: str):
    """
    Retrieve all attendance records for a specific student.
    """
    records = await get_student_attendance_history_service(student_id)
    if not records:
        raise HTTPException(status_code=404, detail="No attendance records found.")
    return {"student_id": student_id, "records": records}


@router.post("/recognize")
async def recognize_and_mark_attendance(image: UploadFile = File(...)):
    """
    Upload a face image → recognize the student → mark attendance automatically.
    """
    image_bytes = await image.read()
    student = await recognize_face_service(image_bytes)

    if not student:
        raise HTTPException(status_code=404, detail="No matching face found.")

    student_id = student["student_id"]
    result = await mark_attendance_service(student_id, "present")

    return {
        "message": f"Attendance marked for {student['name']}",
        "student": student,
        "attendance": result,
    }
