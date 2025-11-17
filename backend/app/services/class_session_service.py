from bson import ObjectId
from datetime import datetime
from app.database.connection import db

class_sessions = db["class_sessions"]
classes = db["classes"]


def session_helper(s):
    return {
        "id": str(s["_id"]),
        "class_id": s["class_id"],
        "session_date": s["session_date"],
        "status": s["status"],
        "attendance_marked": s["attendance_marked"],
        "created_at": s["created_at"]
    }


async def create_class_session_service(class_id: str):
    try:
        class_obj = await classes.find_one({"_id": ObjectId(class_id)})
        if not class_obj:
            return None, "Class not found"

        doc = {
            "class_id": class_id,
            "session_date": datetime.utcnow(),
            "status": "ongoing",
            "attendance_marked": False,
            "created_at": datetime.utcnow()
        }

        result = await class_sessions.insert_one(doc)
        new_s = await class_sessions.find_one({"_id": result.inserted_id})
        return session_helper(new_s), None

    except:
        return None, "Invalid class_id"
