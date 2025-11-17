"""
Image preprocessing utilities for YOLO and ArcFace models.
Handles resizing, color conversion, and normalization.
"""
import cv2
import numpy as np
from .models import get_yolo_input_size, get_arcface_input_size


def preprocess_for_yolo(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image for YOLO face detection.
    Uses dynamic input size from model metadata.

    Args:
        image: Input image in BGR format

    Returns:
        Preprocessed tensor of shape (1, 3, size, size)
    """
    input_size = get_yolo_input_size()
    resized = cv2.resize(image, (input_size, input_size))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    normalized = rgb.astype(np.float32) / 255.0
    transposed = normalized.transpose(2, 0, 1)[None]
    return transposed


def preprocess_for_arcface(face_img: np.ndarray) -> np.ndarray:
    """
    Preprocess face image for ArcFace embedding extraction.
    Uses dynamic input size from model metadata.

    Args:
        face_img: Face crop in BGR format

    Returns:
        Preprocessed tensor of shape (1, 3, size, size)
    """
    input_size = get_arcface_input_size()
    resized = cv2.resize(face_img, (input_size, input_size))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    normalized = rgb.astype(np.float32) / 127.5 - 1.0
    transposed = normalized.transpose(2, 0, 1)[None]
    return transposed


def preprocess_for_arcface_batch(face_imgs: list[np.ndarray]) -> np.ndarray:
    """
    Batch preprocess multiple faces for ArcFace.
    Significantly faster than processing one at a time.

    Args:
        face_imgs: List of face image crops (BGR format)

    Returns:
        Batched preprocessed tensor of shape (N, 3, size, size)
    """
    if len(face_imgs) == 0:
        return np.array([])

    input_size = get_arcface_input_size()
    batch = []

    for face_img in face_imgs:
        resized = cv2.resize(face_img, (input_size, input_size))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        normalized = rgb.astype(np.float32) / 127.5 - 1.0
        transposed = normalized.transpose(2, 0, 1)
        batch.append(transposed)

    return np.array(batch)
