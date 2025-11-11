import os
from dotenv import load_dotenv

# Load variables from the .env file in the project root
load_dotenv()

# Read connection details from environment variables
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DATABASE_NAME")

# Basic sanity check (optional but useful for debugging)
if not MONGO_URI or not DB_NAME:
    raise ValueError("❌ Missing MongoDB configuration: Check your .env file.")
