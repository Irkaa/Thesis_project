import motor.motor_asyncio
from app.utils.config import MONGO_URI, DB_NAME

# Initialize MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

# Access specific database
db = client[DB_NAME]

# Define your collections
student_collection = db["students"]
attendance_collection = db["attendance"]
user_collection = db["users"]
