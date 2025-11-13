import os
from dotenv import load_dotenv

# Load variables from the .env file in the project root
load_dotenv()

# Read connection details from environment variables
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DATABASE_NAME")

# AWS configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Basic sanity check (optional but useful for debugging)
if not MONGO_URI or not DB_NAME:
    raise ValueError("❌ Missing MongoDB configuration: Check your .env file.")
