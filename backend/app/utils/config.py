import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "attendance_system")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in .env file!")
if len(SECRET_KEY) < 32:
    print("⚠️  WARNING: SECRET_KEY should be at least 32 characters long!")

# Application
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Face Recognition Models (NEW)
YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "/app/models/yolov8n-face.onnx")
ARCFACE_MODEL_PATH = os.getenv("ARCFACE_MODEL_PATH", "/app/models/arcface_resnet100.onnx")

# Face Recognition Thresholds (NEW)
FACE_DETECTION_THRESHOLD = float(os.getenv("FACE_DETECTION_THRESHOLD", "0.45"))
RECOGNITION_MATCH_THRESHOLD = float(os.getenv("RECOGNITION_MATCH_THRESHOLD", "0.32"))

# Upload Settings
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB

# Token
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))