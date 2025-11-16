from fastapi import APIRouter, HTTPException
from app.database.schemas import ClassSessionBase, ClassSessionUpdate
from app.services.class_session_service import (
    create_class_session_service,
    get_all_sessions_service,
    get_session_by_id_service,
    update_session_service,
    delete_session_service
)

router = APIRouter(prefix="/class-sessions", tags=["Class Sessions"])


@router.post("/")
async def create_session(payload: ClassSessionBase):
    result = await create_class_session_service(payload.dict())

    if result == "CLASS_NOT_FOUND":
        raise HTTPException(status_code=404, detail="Class not found")

    return result


@router.get("/")
async def get_sessions():
    return await get_all_sessions_service()


@router.get("/{session_id}")
async def get_session(session_id: str):
    sess = await get_session_by_id_service(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return sess


@router.put("/{session_id}")
async def update_session(session_id: str, payload: ClassSessionUpdate):
    result = await update_session_service(
        session_id, payload.dict(exclude_none=True)
    )

    if result == "INVALID_CLASS_ID":
        raise HTTPException(status_code=400, detail="Invalid class_id")

    if result == "CLASS_NOT_FOUND":
        raise HTTPException(status_code=404, detail="Class not found")

    if not result:
        raise HTTPException(status_code=404, detail="Session not found")

    return result


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    deleted = await delete_session_service(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}
