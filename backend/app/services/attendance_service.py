from datetime import datetime
from app.database.connection import db
from app.database.models import attendance_helper

attendance_collection = db["attendance"]
student_collection = db["students"]

def get_today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")

async def mark_attendance_service(student_id: str, status: str):
    """Mark or update a student's attendance for today."""
    student = await student_collection.find_one({"student_id": student_id})
    if not student:
        return None

    today = get_today_str()

    existing = await attendance_collection.find_one({"student_id": student_id, "date": today})
    if existing:
        await attendance_collection.update_one(
            {"_id": existing["_id"]},
            {"$set": {"status": status}}
        )
        updated = await attendance_collection.find_one({"_id": existing["_id"]})
        return attendance_helper(updated)

    record = {
        "student_id": student_id,
        "date": today,
        "status": status,
    }
    new_record = await attendance_collection.insert_one(record)
    created = await attendance_collection.find_one({"_id": new_record.inserted_id})
    return attendance_helper(created)

async def get_attendance_by_date_service(date: str):
    """Retrieve all attendance records for a specific date."""
    records = []
    async for record in attendance_collection.find({"date": date}):
        records.append(attendance_helper(record))
    return records

async def get_student_attendance_history_service(student_id: str):
    """Retrieve attendance history for a specific student."""
    records = []
    async for record in attendance_collection.find({"student_id": student_id}):
        records.append(attendance_helper(record))
    return records
