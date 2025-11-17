"""
Face Recognition Package
========================

Modular face detection and recognition system using YOLO and ArcFace.

Public API:
- detect_single_face: Detect one face in an image
- detect_multiple_faces: Detect multiple faces in an image
- extract_embedding: Extract embedding from a single face
- extract_embeddings_batch: Batch extract embeddings from multiple faces

Usage:
    from app.services.face_recognition import detect_multiple_faces, extract_embeddings_batch

    # Detect faces
    faces = detect_multiple_faces(image)

    # Extract embeddings in batch
    face_crops = [crop for _, _, _, _, _, crop in faces]
    embeddings = extract_embeddings_batch(face_crops)
"""

from .yolo_detector import detect_single_face, detect_multiple_faces
from .arcface_embedder import extract_embedding, extract_embeddings_batch

__all__ = [
    "detect_single_face",
    "detect_multiple_faces",
    "extract_embedding",
    "extract_embeddings_batch",
]

__version__ = "1.0.0"
