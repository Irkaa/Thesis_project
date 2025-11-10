from fastapi import APIRouter
from app.database.connection import db

router = APIRouter()

@router.get("/test_db")
async def test_db_connection():
    try:
        # Try fetching all collections
        collections = await db.list_collection_names()
        return {"status": "Connected", "collections": collections}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}
