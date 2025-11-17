from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.config import MONGO_URI, DB_NAME

# Create async MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

# Export db as alias for compatibility
db = database

# Define all collections
student_collection = database.get_collection("students")
attendance_collection = database.get_collection("attendance")
user_collection = database.get_collection("users")
class_collection = database.get_collection("classes")
class_session_collection = database.get_collection("class_sessions")
student_embedding_collection = database.get_collection("student_embeddings")
recognition_log_collection = database.get_collection("recognition_logs")