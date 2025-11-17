"""
YOLO-based face detection.
Handles face detection, bounding box parsing, and NMS.
"""
import cv2
import numpy as np
import logging
from app.utils.config import FACE_DETECTION_THRESHOLD
from .models import (
    get_yolo_session,
    get_yolo_input_name,
    get_yolo_input_size,
    get_yolo_output_format,
    inspect_yolo_model
)
from .nms import apply_nms
from .preprocessors import preprocess_for_yolo

logger = logging.getLogger(__name__)


def _parse_yolo_output(outputs, orig_width, orig_height):
    """
    Parse YOLO ONNX output and convert to standardized format.
    Handles multiple YOLOv8 export formats.

    Args:
        outputs: raw ONNX session output
        orig_width: original image width
        orig_height: original image height

    Returns:
        boxes: numpy array of shape (N, 4) with [x1, y1, x2, y2] in original image coords
        scores: numpy array of shape (N,) with confidence scores
    """
    model_input_size = get_yolo_input_size()

    # Handle different output formats
    if len(outputs) == 1:
        # Single output - most common for YOLOv8
        pred = outputs[0]

        # Expected shapes:
        # (1, N, 5+classes) - batch, predictions, [cx, cy, w, h, conf, ...]
        # (N, 5+classes)    - predictions, [cx, cy, w, h, conf, ...]
        # (1, 5+classes, N) - batch, features, predictions (transposed)

        # Remove batch dimension if present
        if len(pred.shape) == 3:
            pred = pred[0]

        # Transpose if needed: (features, N) -> (N, features)
        if pred.shape[0] < pred.shape[1] and pred.shape[0] < 100:
            pred = pred.T

        # Now pred should be (N, 5+classes)
        if pred.shape[1] < 5:
            raise ValueError(f"Unexpected YOLO output shape: {pred.shape}")

        # Extract boxes and scores
        # YOLOv8-face format: [cx, cy, w, h, confidence]
        # Note: YOLOv8-face has only ONE class (face), so no class scores
        boxes_cxcywh = pred[:, :4]  # center_x, center_y, width, height
        confidence = pred[:, 4]      # objectness score

        # FIX: For single-class models (like YOLOv8-face), use confidence directly
        # Don't multiply by class scores as class is always 1.0
        scores = confidence

        # Convert from cx,cy,w,h (normalized to model_input_size) to x1,y1,x2,y2 (original image)
        cx = boxes_cxcywh[:, 0]
        cy = boxes_cxcywh[:, 1]
        w = boxes_cxcywh[:, 2]
        h = boxes_cxcywh[:, 3]

        # Use dynamic scaling based on actual model input size
        scale_x = orig_width / float(model_input_size)
        scale_y = orig_height / float(model_input_size)

        x1 = (cx - w / 2) * scale_x
        y1 = (cy - h / 2) * scale_y
        x2 = (cx + w / 2) * scale_x
        y2 = (cy + h / 2) * scale_y

        boxes = np.stack([x1, y1, x2, y2], axis=1)

    elif len(outputs) == 2:
        # Dual output - boxes and scores separate
        boxes_out = outputs[0]
        scores_out = outputs[1]

        # Remove batch dimensions
        if len(boxes_out.shape) == 3:
            boxes_out = boxes_out[0]
        if len(scores_out.shape) == 3:
            scores_out = scores_out[0]

        # Convert and scale boxes
        boxes = boxes_out.copy()
        scores = scores_out.flatten() if scores_out.ndim > 1 else scores_out

        # Use dynamic scaling
        scale_x = orig_width / float(model_input_size)
        scale_y = orig_height / float(model_input_size)
        boxes[:, [0, 2]] *= scale_x
        boxes[:, [1, 3]] *= scale_y
    else:
        raise ValueError(f"Unsupported YOLO output format: {len(outputs)} outputs")

    return boxes, scores


def detect_single_face(image: np.ndarray) -> np.ndarray | None:
    """
    Detect single face in image (for enrollment).
    Returns cropped face or None if no face detected.

    Uses NMS to handle multiple detections and returns the highest confidence face.

    Args:
        image: Input image in BGR format

    Returns:
        Cropped face image or None
    """
    h, w = image.shape[:2]
    preprocessed = preprocess_for_yolo(image)

    yolo_session = get_yolo_session()
    input_name = get_yolo_input_name()

    # Run inference
    raw_outputs = yolo_session.run(None, {input_name: preprocessed})

    # Inspect model on first run
    if get_yolo_output_format() is None:
        inspect_yolo_model()

    # Parse outputs to standardized format
    try:
        boxes, scores = _parse_yolo_output(raw_outputs, w, h)
    except Exception as e:
        logger.error(f"Failed to parse YOLO output: {e}")
        return None

    # Filter by confidence threshold
    mask = scores >= FACE_DETECTION_THRESHOLD
    boxes = boxes[mask]
    scores = scores[mask]

    if len(boxes) == 0:
        return None

    # Apply NMS to remove duplicates
    keep_indices = apply_nms(boxes, scores, iou_threshold=0.45)

    if len(keep_indices) == 0:
        return None

    # Take highest confidence detection after NMS
    best_idx = keep_indices[np.argmax(scores[keep_indices])]
    x1, y1, x2, y2 = boxes[best_idx]

    # Convert to integers and clamp to image boundaries
    x1 = int(max(0, min(x1, w - 1)))
    y1 = int(max(0, min(y1, h - 1)))
    x2 = int(max(0, min(x2, w)))
    y2 = int(max(0, min(y2, h)))

    # Ensure valid box
    if x2 <= x1 or y2 <= y1:
        return None

    face_crop = image[y1:y2, x1:x2]

    # Verify crop is not empty
    if face_crop.size == 0:
        return None

    return face_crop


def detect_multiple_faces(image: np.ndarray) -> list[tuple]:
    """
    Detect multiple faces in image (for classroom attendance).
    Returns list of (x1, y1, x2, y2, confidence, face_crop).

    Applies NMS to remove duplicate detections of the same person.

    Args:
        image: Input image in BGR format

    Returns:
        List of tuples containing bounding box, confidence, and face crop
    """
    h, w = image.shape[:2]
    preprocessed = preprocess_for_yolo(image)

    yolo_session = get_yolo_session()
    input_name = get_yolo_input_name()

    # Run inference
    raw_outputs = yolo_session.run(None, {input_name: preprocessed})

    # Inspect model on first run
    if get_yolo_output_format() is None:
        inspect_yolo_model()

    # Parse outputs to standardized format
    try:
        boxes, scores = _parse_yolo_output(raw_outputs, w, h)
    except Exception as e:
        logger.error(f"Failed to parse YOLO output: {e}")
        return []

    # Filter by confidence threshold
    mask = scores >= FACE_DETECTION_THRESHOLD
    boxes = boxes[mask]
    scores = scores[mask]

    if len(boxes) == 0:
        return []

    # Apply NMS to remove duplicate detections
    keep_indices = apply_nms(boxes, scores, iou_threshold=0.45)

    if len(keep_indices) == 0:
        return []

    # Build result list
    faces = []
    for idx in keep_indices:
        x1, y1, x2, y2 = boxes[idx]
        score = scores[idx]

        # Convert to integers and clamp to image boundaries
        x1 = int(max(0, min(x1, w - 1)))
        y1 = int(max(0, min(y1, h - 1)))
        x2 = int(max(0, min(x2, w)))
        y2 = int(max(0, min(y2, h)))

        # Ensure valid box
        if x2 <= x1 or y2 <= y1:
            continue

        face_crop = image[y1:y2, x1:x2]

        # Skip if crop is empty
        if face_crop.size == 0:
            continue

        faces.append((x1, y1, x2, y2, float(score), face_crop))

    logger.info(f"Detected {len(faces)} faces after NMS (from {len(boxes)} raw detections)")

    return faces
