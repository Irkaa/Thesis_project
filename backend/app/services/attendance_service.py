from datetime import datetime
from bson import ObjectId
from app.database.connection import db

attendance_collection = db["attendance"]
class_sessions_collection = db["class_sessions"]
students_collection = db["students"]
recognition_logs_collection = db["recognition_logs"]


async def mark_attendance_service(student_id: str, status: str):
    """
    Manual attendance marking.
    """

    if status not in ["present", "absent"]:
        raise ValueError("Invalid attendance status")

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


async def mark_attendance_from_recognition(class_session_id: str, detected_student_ids: list):
    """
    Marks all class students present/absent based on recognition result.
    """

    if not ObjectId.is_valid(class_session_id):
        raise ValueError("Invalid class_session_id")

    session = await class_sessions_collection.find_one({"_id": ObjectId(class_session_id)})
    if not session:
        raise ValueError("Class session not found")

    class_id = session["class_id"]

    students_cursor = students_collection.find({"class_id": class_id})
    all_students = [str(s["_id"]) async for s in students_cursor]

    present = []
    absent = []

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


async def get_attendance_by_student_service(student_id: str):
    """
    Get all attendance records for a specific student.
    """
    if not ObjectId.is_valid(student_id):
        raise ValueError("Invalid student_id")

    # Find all attendance records for this student
    attendance_cursor = attendance_collection.find({"student_id": student_id})
    attendance_records = []

    async for record in attendance_cursor:
        # Get session details
        session = None
        if "class_session_id" in record and ObjectId.is_valid(record["class_session_id"]):
            session = await class_sessions_collection.find_one({"_id": ObjectId(record["class_session_id"])})

        attendance_records.append({
            "student_id": record.get("student_id"),
            "class_session_id": record.get("class_session_id"),
            "present": record.get("present"),
            "timestamp": record.get("timestamp"),
            "session_date": session.get("session_date") if session else None
        })

    return {
        "student_id": student_id,
        "total_records": len(attendance_records),
        "attendance": attendance_records
    }


async def get_attendance_by_session_service(session_id: str):
    """
    Get all attendance records for a specific class session.
    """
    if not ObjectId.is_valid(session_id):
        raise ValueError("Invalid session_id")

    # Verify session exists
    session = await class_sessions_collection.find_one({"_id": ObjectId(session_id)})
    if not session:
        raise ValueError("Class session not found")

    # Find all attendance records for this session
    attendance_cursor = attendance_collection.find({"class_session_id": session_id})
    attendance_records = []

    async for record in attendance_cursor:
        # Get student details
        student = None
        if "student_id" in record and ObjectId.is_valid(record["student_id"]):
            student = await students_collection.find_one({"_id": ObjectId(record["student_id"])})

        attendance_records.append({
            "student_id": record.get("student_id"),
            "student_name": student.get("name") if student else None,
            "present": record.get("present"),
            "timestamp": record.get("timestamp")
        })

    # Calculate statistics
    total_students = len(attendance_records)
    present_count = sum(1 for r in attendance_records if r["present"])
    absent_count = total_students - present_count

    return {
        "session_id": session_id,
        "session_date": session.get("session_date"),
        "total_students": total_students,
        "present_count": present_count,
        "absent_count": absent_count,
        "attendance": attendance_records
    }
