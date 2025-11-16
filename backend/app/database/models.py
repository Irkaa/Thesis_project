from bson import ObjectId

# Helper function to convert MongoDB document (_id as ObjectId) to a JSON-serializable dict
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "student_id": student["student_id"],
        "name": student["name"],
        "email": student["email"],
        "class_name": student["class_name"],
        "photo_url": student.get("photo_url"),
    }


# (Optional) You can also define other helpers later, such as attendance or user models.
def attendance_helper(record) -> dict:
    return {
        "id": str(record["_id"]),
        "student_id": record["student_id"],
        "date": record["date"],
        "status": record["status"],
    }


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user.get("role", "teacher"),
    }


def class_helper(class_doc) -> dict:
    return {
        "class_id": str(class_doc["_id"]),
        "class_name": class_doc.get("class_name"),
        "teacher_id": class_doc.get("teacher_id"),
        "semester": class_doc.get("semester"),
        "department": class_doc.get("department"),
    }


def class_session_helper(doc) -> dict:
    return {
        "session_id": str(doc["_id"]),
        "class_id": doc.get("class_id"),
        "date": doc.get("date"),
        "start_time": doc.get("start_time"),
        "end_time": doc.get("end_time"),
        "location": doc.get("location"),
        "session_type": doc.get("session_type"),
    }


def recognition_log_helper(doc) -> dict:
    return {
        "log_id": str(doc["_id"]),
        "student_id": doc.get("student_id"),
        "event_time": doc.get("event_time").isoformat() if doc.get("event_time") else None,
        "confidence": doc.get("confidence"),
        "camera_id": doc.get("camera_id"),
        "status": doc.get("status"),
        "raw_face_capture_s3_url": doc.get("raw_face_capture_s3_url"),
        "embedding_vector": doc.get("embedding_vector"),
        "matched_student_id": doc.get("matched_student_id"),
        "distance_score": doc.get("distance_score"),
        "session_id": doc.get("session_id"),
    }
# event_time is converted to ISO string for JSON safety.

def student_embedding_helper(doc) -> dict:
    return {
        "embedding_id": str(doc["_id"]),
        "student_id": doc.get("student_id"),
        "embedding": doc.get("embedding"),
        "photo_s3_url": doc.get("photo_s3_url"),
        "version": doc.get("version"),
        "created_at": doc.get("created_at"),
    }


def attendance_helper(doc) -> dict:
    return {
        "attendance_id": str(doc["_id"]),
        "student_id": doc.get("student_id"),
        "session_id": doc.get("session_id"),
        "recognized_time": doc.get("recognized_time"),
        "status": doc.get("status"),
        "recognized_confidence": doc.get("recognized_confidence"),
    }
