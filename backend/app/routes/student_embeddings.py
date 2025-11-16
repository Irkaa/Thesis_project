from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.embedding_service import extract_embedding_from_image
from app.services.student_embedding_service import add_student_embedding_service

router = APIRouter(prefix="/students", tags=["Student Embeddings"])


@router.post("/{student_id}/upload-face")
async def upload_face(student_id: str, image: UploadFile = File(...)):
    # Read uploaded file
    image_bytes = await image.read()

    # Extract embedding
    embedding = extract_embedding_from_image(image_bytes)

    if embedding is None:
        raise HTTPException(status_code=400, detail="No face detected in image")

    # Save embedding (S3 will be added later)
    result = await add_student_embedding_service(
        student_id=student_id,
        embedding=embedding,
        photo_url=None
    )

    return {
        "message": "Student face registered successfully",
        "embedding_saved": True,
        "embedding_id": result["embedding_id"],
        "student_id": result["student_id"]
    }
