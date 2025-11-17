"""
Student enrollment service.
Handles single face photo uploads for student registration.
"""
import cv2
import numpy as np
from app.services.face_recognition import (
    detect_single_face,
    extract_embedding
)


def generate_embedding_from_image(image_bytes: bytes) -> list[float] | None:
    """
    Generate face embedding from uploaded student photo.
    Used during student enrollment by admin.
    
    Args:
        image_bytes: Image file bytes
        
    Returns:
        512-dim embedding vector or None if no face detected
    """
    # Decode image
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    
    if img is None:
        return None
    
    # Detect single face
    face_crop = detect_single_face(img)
    if face_crop is None:
        return None
    
    # Extract embedding
    embedding = extract_embedding(face_crop)
    return embedding