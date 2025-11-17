"""
Classroom attendance recognition service.
Handles multiple faces in classroom photos.
"""
import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.database.connection import student_embedding_collection
from app.services.face_recognition import (
    detect_multiple_faces,
    extract_embedding,
    extract_embeddings_batch
)
from app.utils.config import RECOGNITION_MATCH_THRESHOLD


async def match_embedding(embedding: list[float], threshold: float = None) -> tuple[str | None, float]:
    """
    Match face embedding against all stored student embeddings.
    
    Args:
        embedding: 512-dim face embedding
        threshold: Minimum similarity score (uses config default if None)
        
    Returns:
        (student_id, confidence_score) or (None, best_score)
    """
    if threshold is None:
        threshold = RECOGNITION_MATCH_THRESHOLD
    
    best_id = None
    best_score = 0.0
    
    cursor = student_embedding_collection.find({})
    async for doc in cursor:
        stored = np.array(doc["embedding"])
        score = cosine_similarity([embedding], [stored])[0][0]
        
        if score > best_score:
            best_score = score
            best_id = str(doc["student_id"])
    
    if best_score < threshold:
        return None, best_score
    
    return best_id, best_score


async def recognize_single_image(image_bytes: bytes) -> list[dict]:
    """
    Recognize all faces in a single classroom photo.
    OPTIMIZATION: Uses batch embedding extraction for all detected faces.

    Args:
        image_bytes: Image file bytes

    Returns:
        List of detections with bbox, confidence, student_id
    """
    # Decode image
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if img is None:
        return []

    # Detect all faces
    faces = detect_multiple_faces(img)

    if len(faces) == 0:
        return []

    # OPTIMIZATION: Extract all embeddings in a single batch
    face_crops = [face_crop for _, _, _, _, _, face_crop in faces]

    try:
        embeddings = extract_embeddings_batch(face_crops)
    except ValueError as e:
        # Fallback to single extraction if batch fails
        print(f"Batch embedding extraction failed: {e}, falling back to single mode")
        embeddings = []
        for face_crop in face_crops:
            try:
                embedding = extract_embedding(face_crop)
                embeddings.append(embedding)
            except ValueError:
                embeddings.append(None)

    # Match each embedding against database
    results = []
    for (x1, y1, x2, y2, det_conf, face_crop), embedding in zip(faces, embeddings):
        if embedding is None:
            # Skip invalid embeddings
            continue

        # Match against database
        student_id, match_conf = await match_embedding(embedding)

        results.append({
            "bbox": [x1, y1, x2, y2],
            "detection_confidence": det_conf,
            "match_confidence": match_conf,
            "student_id": student_id
        })

    return results


async def recognize_multiple_images(images_bytes_list: list[bytes]) -> dict:
    """
    Recognize faces across multiple classroom photos.
    Uses majority voting for robustness.
    
    Args:
        images_bytes_list: List of image file bytes
        
    Returns:
        {
            "detected_students": list of unique student_ids,
            "all_detections": list of all detection details,
            "vote_counts": dict of student_id -> detection_count
        }
    """
    all_detections = []
    vote_counts = {}
    
    # Process each image
    for img_bytes in images_bytes_list:
        detections = await recognize_single_image(img_bytes)
        
        for det in detections:
            all_detections.append(det)
            
            student_id = det["student_id"]
            if student_id:
                vote_counts[student_id] = vote_counts.get(student_id, 0) + 1
    
    # Sort by vote count (most detected first)
    sorted_students = sorted(
        vote_counts.items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    detected_students = [sid for sid, count in sorted_students]
    
    return {
        "detected_students": detected_students,
        "all_detections": all_detections,
        "vote_counts": vote_counts
    }