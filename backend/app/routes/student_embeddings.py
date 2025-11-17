from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.embedding_service import generate_embedding_from_image
from app.services.student_embedding_service import add_student_embedding_service
from app.utils.rbac import AdminOnly

router = APIRouter(prefix="/student-embeddings", tags=["Student Embeddings"])


@router.post("/{student_id}", dependencies=[Depends(AdminOnly)])
async def upload_embedding(student_id: str, file: UploadFile = File(...)):
    """Upload student face embedding - Admin only"""
    image_bytes = await file.read()

    embedding = generate_embedding_from_image(image_bytes)
    if embedding is None:
        raise HTTPException(status_code=400, detail="No face detected in the image")

    result = await add_student_embedding_service(student_id, embedding)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )

    return {
        "message": "Embedding stored successfully",
        "embedding": result
    }
