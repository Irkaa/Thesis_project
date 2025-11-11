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
