from app.database.connection import db
from app.database.models import recognition_log_helper
from fastapi import HTTPException, status
from bson import ObjectId, errors
from datetime import datetime

log_collection = db["recognition_logs"]


async def create_recognition_log_service(payload: dict):
    """
    Insert a recognition log. If event_time not provided, set to now.
    Expects payload keys matching RecognitionLogCreate.
    """
    try:
        if not payload.get("event_time"):
            payload["event_time"] = datetime.utcnow()

        result = await log_collection.insert_one(payload)
        created = await log_collection.find_one({"_id": result.inserted_id})
        if not created:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to create recognition log.")
        return recognition_log_helper(created)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error creating recognition log: {str(e)}")


async def get_all_recognition_logs_service(limit: int = 100):
    try:
        logs = []
        cursor = log_collection.find().sort("event_time", -1).limit(limit)
        async for doc in cursor:
            logs.append(recognition_log_helper(doc))
        return logs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error retrieving recognition logs: {str(e)}")


async def get_recognition_log_by_id_service(log_id: str):
    try:
        if not ObjectId.is_valid(log_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid log_id format.")
        doc = await log_collection.find_one({"_id": ObjectId(log_id)})
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Recognition log not found.")
        return recognition_log_helper(doc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error retrieving recognition log: {str(e)}")


async def get_recognition_logs_by_student_service(student_id: str, limit: int = 100):
    try:
        logs = []
        cursor = log_collection.find({"student_id": student_id}).sort("event_time", -1).limit(limit)
        async for doc in cursor:
            logs.append(recognition_log_helper(doc))
        return logs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error retrieving logs for student {student_id}: {str(e)}")


async def get_recognition_logs_by_session_service(session_id: str, limit: int = 100):
    try:
        logs = []
        # session_id in logs is stored as string (matching ERD), but allow ObjectId fallback
        query = {"session_id": session_id}
        if ObjectId.is_valid(session_id):
            # also check logs stored with ObjectId
            query = {"$or": [{"session_id": session_id}, {"session_id": ObjectId(session_id)}]}

        cursor = log_collection.find(query).sort("event_time", -1).limit(limit)
        async for doc in cursor:
            logs.append(recognition_log_helper(doc))
        return logs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error retrieving logs for session {session_id}: {str(e)}")


async def delete_recognition_log_service(log_id: str):
    try:
        if not ObjectId.is_valid(log_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid log_id format.")
        result = await log_collection.delete_one({"_id": ObjectId(log_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Recognition log not found or already deleted.")
        return {"status": "deleted", "log_id": log_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error deleting recognition log: {str(e)}")
