from datetime import datetime
from bson import ObjectId
from app.database.connection import db

# Collections
attendance_collection = db["attendance"]
class_sessions_collection = db["class_sessions"]
students_collection = db["students"]
recognition_logs_collection = db["recognition_logs"]


# -----------------------------------------------------------
# 1) Manual attendance (if you need it later)
# -----------------------------------------------------------
async def mark_attendance_service(student_id: str, status: str):
    """
    Manually mark a student's attendance.
    status: 'present' or 'absent'
    """

    if status not in ["present", "absent"]:
        raise ValueError("Invalid attendance status")

    # Create or update attendance record
    result = await attendance_collection.update_one(
        {"student_id": student_id},
        {
            "$set": {
                "present": (status == "present"),
                "timestamp": datetime.utcnow()
            }
        },
        upsert=True
    )

    return {
        "student_id": student_id,
        "present": (status == "present"),
        "timestamp": datetime.utcnow()
    }


# -----------------------------------------------------------
# 2) Recognition-based attendance (the important part)
# -----------------------------------------------------------
async def mark_attendance_from_recognition(class_session_id: str, detected_student_ids: list):
    """
    Takes a class_session_id and a list of recognized student_ids,
    then marks present/absent for all students in that class.
    """

    # Validate session ID
    if not ObjectId.is_valid(class_session_id):
        raise ValueError("Invalid class_session_id")

    # Fetch session
    session = await class_sessions_collection.find_one({"_id": ObjectId(class_session_id)})
    if not session:
        raise ValueError("Class session not found")

    class_id = session["class_id"]

    # Fetch all students who belong to the class
    students_cursor = students_collection.find({"class_id": class_id})
    all_students = [str(s["_id"]) async for s in students_cursor]

    present = []
    absent = []

    # Loop through each student in the class and mark presence/absence
    for sid in all_students:
        if sid in detected_student_ids:
            present.append(sid)

            await attendance_collection.update_one(
                {"student_id": sid, "class_session_id": class_session_id},
                {
                    "$set": {
                        "present": True,
                        "timestamp": datetime.utcnow()
                    }
                },
                upsert=True
            )

        else:
            absent.append(sid)

            await attendance_collection.update_one(
                {"student_id": sid, "class_session_id": class_session_id},
                {
                    "$set": {
                        "present": False,
                        "timestamp": datetime.utcnow()
                    }
                },
                upsert=True
            )

    # Save recognition log for auditing/debugging
    await recognition_logs_collection.insert_one({
        "class_session_id": class_session_id,
        "detected_students": detected_student_ids,
        "timestamp": datetime.utcnow()
    })

    return {
        "class_session_id": class_session_id,
        "present": present,
        "absent": absent,
        "total_students": len(all_students)
    }
