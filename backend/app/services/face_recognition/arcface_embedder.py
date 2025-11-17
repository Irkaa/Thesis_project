"""
ArcFace-based embedding extraction.
Handles single and batch face embedding generation.
"""
import numpy as np
import logging
from .models import get_arcface_session, get_arcface_input_name
from .preprocessors import preprocess_for_arcface, preprocess_for_arcface_batch

logger = logging.getLogger(__name__)


def extract_embedding(face_img: np.ndarray) -> list[float]:
    """
    Extract 512-dimensional embedding from face image.
    Returns normalized embedding vector.

    Args:
        face_img: Face crop in BGR format

    Returns:
        Normalized 512-dim embedding as list

    Raises:
        ValueError: If face image is invalid or embedding extraction fails
    """
    # Validate input
    if face_img is None or face_img.size == 0:
        raise ValueError("Invalid face image: empty or None")

    preprocessed = preprocess_for_arcface(face_img)

    arcface_session = get_arcface_session()
    input_name = get_arcface_input_name()
    embedding = arcface_session.run(None, {input_name: preprocessed})[0]

    # L2 normalization with zero-norm guard
    embedding = embedding.flatten()
    norm = np.linalg.norm(embedding)

    # Guard against zero-length embeddings (avoid divide-by-zero)
    if norm < 1e-6:
        raise ValueError("Zero-norm embedding detected - face may be invalid or model error")

    normalized = embedding / norm

    return normalized.tolist()


def extract_embeddings_batch(face_imgs: list[np.ndarray]) -> list[list[float]]:
    """
    Batch extract embeddings from multiple face images.
    Significantly faster than calling extract_embedding() in a loop.

    Args:
        face_imgs: List of face image crops

    Returns:
        List of normalized embedding vectors

    Raises:
        ValueError: If any face image is invalid
    """
    if len(face_imgs) == 0:
        return []

    # Validate all inputs
    for i, face_img in enumerate(face_imgs):
        if face_img is None or face_img.size == 0:
            raise ValueError(f"Invalid face image at index {i}: empty or None")

    # Batch preprocess all faces
    preprocessed_batch = preprocess_for_arcface_batch(face_imgs)

    # Run batch inference
    arcface_session = get_arcface_session()
    input_name = get_arcface_input_name()
    embeddings_batch = arcface_session.run(None, {input_name: preprocessed_batch})[0]

    # L2 normalize each embedding
    normalized_embeddings = []
    for i, embedding in enumerate(embeddings_batch):
        embedding = embedding.flatten()
        norm = np.linalg.norm(embedding)

        # Guard against zero-length embeddings
        if norm < 1e-6:
            raise ValueError(f"Zero-norm embedding detected at index {i} - face may be invalid or model error")

        normalized = embedding / norm
        normalized_embeddings.append(normalized.tolist())

    logger.info(f"Batch extracted {len(normalized_embeddings)} embeddings")

    return normalized_embeddings
