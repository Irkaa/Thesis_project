from datetime import datetime
from app.database.connection import db

recognition_logs = db["recognition_logs"]


def recognition_log_helper(log):
    return {
        "id": str(log["_id"]),
        "detections": log["detections"],
        "uploaded_by": log["uploaded_by"],
        "class_id": log.get("class_id"),
        "session_id": log.get("session_id"),
        "timestamp": log["timestamp"]
    }


async def save_recognition_log(
    detections: list,
    uploaded_by: str,
    class_id: str | None = None,
    session_id: str | None = None
):
    log = {
        "detections": detections,
        "uploaded_by": uploaded_by,
        "class_id": class_id,
        "session_id": session_id,
        "timestamp": datetime.utcnow()
    }

    result = await recognition_logs.insert_one(log)
    saved = await recognition_logs.find_one({"_id": result.inserted_id})
    return recognition_log_helper(saved)


async def get_all_logs_service():
    logs = []
    async for log in recognition_logs.find().sort("timestamp", -1):
        logs.append(recognition_log_helper(log))
    return logs


async def get_logs_for_class_service(class_id: str):
    logs = []
    async for log in recognition_logs.find({"class_id": class_id}).sort("timestamp", -1):
        logs.append(recognition_log_helper(log))
    return logs


async def get_logs_for_session_service(session_id: str):
    logs = []
    async for log in recognition_logs.find({"session_id": session_id}).sort("timestamp", -1):
        logs.append(recognition_log_helper(log))
    return logs
