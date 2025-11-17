"""
Database model helpers - converts MongoDB documents to JSON.
"""
from datetime import datetime


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "student_id": student["student_id"],
        "name": student["name"],
        "email": student.get("email"),
        "class_id": student.get("class_id"),
        "class_name": student.get("class_name"),
        "photo_url": student.get("photo_url"),
        "created_at": student.get("created_at")
    }


def attendance_helper(attendance) -> dict:
    """Single definition with all fields"""
    return {
        "id": str(attendance["_id"]),
        "student_id": attendance["student_id"],
        "class_session_id": attendance.get("class_session_id"),
        "present": attendance["present"],
        "timestamp": attendance["timestamp"]
    }


def user_helper(user) -> dict:
    """Single definition with all fields"""
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "created_at": user.get("created_at")
    }


def class_helper(c) -> dict:
    return {
        "id": str(c["_id"]),
        "class_name": c["class_name"],
        "teacher_id": c["teacher_id"],
        "student_ids": c.get("student_ids", []),
        "created_at": c.get("created_at")
    }


def class_session_helper(session) -> dict:
    return {
        "id": str(session["_id"]),
        "class_id": session["class_id"],
        "session_date": session["session_date"],
        "status": session["status"],
        "attendance_marked": session["attendance_marked"],
        "created_at": session["created_at"]
    }


def recognition_log_helper(log) -> dict:
    return {
        "id": str(log["_id"]),
        "detections": log["detections"],
        "uploaded_by": log["uploaded_by"],
        "class_id": log.get("class_id"),
        "session_id": log.get("session_id"),
        "timestamp": log["timestamp"].isoformat() if isinstance(log["timestamp"], datetime) else log["timestamp"]
    }


def student_embedding_helper(embedding) -> dict:
    return {
        "id": str(embedding["_id"]),
        "student_id": embedding["student_id"],
        "version": embedding.get("version", 1),
        "photo_s3_url": embedding.get("photo_s3_url"),
        "created_at": embedding.get("created_at")
    }