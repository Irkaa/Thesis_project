from fastapi import APIRouter, HTTPException
from app.database.schemas import ClassBase, ClassUpdate
from app.services.class_service import (
    create_class_service,
    get_all_classes_service,
    get_class_by_id_service,
    update_class_service,
    delete_class_service,
)

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.post("/")
async def create_class(payload: ClassBase):
    return await create_class_service(payload.dict())


@router.get("/")
async def get_classes():
    return await get_all_classes_service()


@router.get("/{class_id}")
async def get_class(class_id: str):
    cls = await get_class_by_id_service(class_id)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    return cls


@router.put("/{class_id}")
async def update_class(class_id: str, payload: ClassUpdate):
    updated = await update_class_service(class_id, payload.dict(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Class not found or invalid ID")
    return updated


@router.delete("/{class_id}")
async def delete_class(class_id: str):
    result = await delete_class_service(class_id)
    if not result:
        raise HTTPException(status_code=404, detail="Class not found or invalid ID")
    return {"status": "deleted"}
