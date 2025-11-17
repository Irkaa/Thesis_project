"""
Shared face recognition functionality.
Loads models once, provides detection and embedding extraction.
"""
import cv2
import numpy as np
import onnxruntime as ort
import logging
from app.utils.config import (
    YOLO_MODEL_PATH,
    ARCFACE_MODEL_PATH,
    FACE_DETECTION_THRESHOLD
)

# Configure logging
logger = logging.getLogger(__name__)

# ========== LOAD MODELS ONCE (SHARED) ==========
_yolo_session = None
_arcface_session = None
_yolo_output_format = None  # Cache detected output format

# OPTIMIZATION: Cache input names and model dimensions (avoid repeated lookups)
_yolo_input_name = None
_yolo_input_size = None
_arcface_input_name = None
_arcface_input_size = None


def _get_yolo_session():
    """Lazy load YOLO model (singleton pattern)"""
    global _yolo_session, _yolo_input_name, _yolo_input_size
    if _yolo_session is None:
        _yolo_session = ort.InferenceSession(
            YOLO_MODEL_PATH,
            providers=["CPUExecutionProvider"]
        )
        # Cache input name and size
        input_meta = _yolo_session.get_inputs()[0]
        _yolo_input_name = input_meta.name
        # Extract input size from shape: typically [batch, 3, height, width]
        shape = input_meta.shape
        if len(shape) == 4:
            _yolo_input_size = shape[2]  # Assume square input (height == width)
            logger.info(f"YOLO input size: {_yolo_input_size}x{_yolo_input_size}")
        else:
            _yolo_input_size = 640  # Fallback to default
            logger.warning(f"Unexpected YOLO input shape: {shape}, defaulting to 640")
    return _yolo_session


def _get_arcface_session():
    """Lazy load ArcFace model (singleton pattern)"""
    global _arcface_session, _arcface_input_name, _arcface_input_size
    if _arcface_session is None:
        _arcface_session = ort.InferenceSession(
            ARCFACE_MODEL_PATH,
            providers=["CPUExecutionProvider"]
        )
        # Cache input name and size
        input_meta = _arcface_session.get_inputs()[0]
        _arcface_input_name = input_meta.name
        # Extract input size from shape: typically [batch, 3, height, width]
        shape = input_meta.shape
        if len(shape) == 4:
            _arcface_input_size = shape[2]  # Assume square input
            logger.info(f"ArcFace input size: {_arcface_input_size}x{_arcface_input_size}")
        else:
            _arcface_input_size = 112  # Fallback to default
            logger.warning(f"Unexpected ArcFace input shape: {shape}, defaulting to 112")
    return _arcface_session


def _get_yolo_input_name():
    """Get cached YOLO input name"""
    if _yolo_input_name is None:
        _get_yolo_session()  # Trigger lazy load
    return _yolo_input_name


def _get_yolo_input_size():
    """Get cached YOLO input size"""
    if _yolo_input_size is None:
        _get_yolo_session()  # Trigger lazy load
    return _yolo_input_size


def _get_arcface_input_name():
    """Get cached ArcFace input name"""
    if _arcface_input_name is None:
        _get_arcface_session()  # Trigger lazy load
    return _arcface_input_name


def _get_arcface_input_size():
    """Get cached ArcFace input size"""
    if _arcface_input_size is None:
        _get_arcface_session()  # Trigger lazy load
    return _arcface_input_size


def _inspect_yolo_model():
    """
    Inspect YOLO model at startup to understand output format.
    Logs input/output shapes for debugging.
    """
    global _yolo_output_format

    session = _get_yolo_session()

    # Log input info
    inputs = session.get_inputs()
    logger.info(f"YOLO Model - Inputs: {len(inputs)}")
    for inp in inputs:
        logger.info(f"  - {inp.name}: shape={inp.shape}, type={inp.type}")

    # Log output info
    outputs = session.get_outputs()
    logger.info(f"YOLO Model - Outputs: {len(outputs)}")
    for out in outputs:
        logger.info(f"  - {out.name}: shape={out.shape}, type={out.type}")

    # Determine output format based on shape
    # Common formats:
    # - (1, N, 5+classes) or (N, 5+classes) - standard YOLOv8
    # - (1, 4, N) and (1, 1, N) - split boxes/scores
    # - (1, N, 6) - simplified with NMS

    if len(outputs) == 1:
        shape = outputs[0].shape
        logger.info(f"Single output detected: {shape}")
        _yolo_output_format = "single"
    elif len(outputs) == 2:
        logger.info("Dual output detected (likely boxes + scores)")
        _yolo_output_format = "dual"
    else:
        logger.warning(f"Unexpected output count: {len(outputs)}")
        _yolo_output_format = "unknown"


def _apply_nms(boxes, scores, iou_threshold=0.45):
    """
    Apply Non-Maximum Suppression to remove duplicate detections.

    Args:
        boxes: numpy array of shape (N, 4) with [x1, y1, x2, y2]
        scores: numpy array of shape (N,) with confidence scores
        iou_threshold: IoU threshold for NMS (default 0.45)

    Returns:
        indices: array of indices to keep after NMS
    """
    if len(boxes) == 0:
        return np.array([])

    # FIX: cv2.dnn.NMSBoxes expects [x, y, w, h] format, not [x1, y1, x2, y2]
    # Convert from corner format to xywh format
    boxes_xywh = []
    for x1, y1, x2, y2 in boxes:
        w = x2 - x1
        h = y2 - y1
        boxes_xywh.append([x1, y1, w, h])

    # Use OpenCV's NMS implementation (fast and reliable)
    indices = cv2.dnn.NMSBoxes(
        bboxes=boxes_xywh,
        scores=scores.tolist(),
        score_threshold=FACE_DETECTION_THRESHOLD,
        nms_threshold=iou_threshold
    )

    # OpenCV returns different formats depending on version
    if len(indices) > 0:
        if isinstance(indices, tuple):
            indices = indices[0]
        indices = indices.flatten()

    return indices


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
    # OPTIMIZATION: Use dynamic model input size instead of hardcoded 640
    model_input_size = _get_yolo_input_size()

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

        # OPTIMIZATION: Use dynamic scaling based on actual model input size
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

        # OPTIMIZATION: Use dynamic scaling
        scale_x = orig_width / float(model_input_size)
        scale_y = orig_height / float(model_input_size)
        boxes[:, [0, 2]] *= scale_x
        boxes[:, [1, 3]] *= scale_y
    else:
        raise ValueError(f"Unsupported YOLO output format: {len(outputs)} outputs")

    return boxes, scores


# ========== SHARED PREPROCESSING ==========
def _preprocess_for_yolo(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image for YOLO face detection.
    OPTIMIZATION: Uses dynamic input size from model metadata.
    """
    input_size = _get_yolo_input_size()
    resized = cv2.resize(image, (input_size, input_size))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    normalized = rgb.astype(np.float32) / 255.0
    transposed = normalized.transpose(2, 0, 1)[None]
    return transposed


def _preprocess_for_arcface(face_img: np.ndarray) -> np.ndarray:
    """
    Preprocess face image for ArcFace embedding extraction.
    OPTIMIZATION: Uses dynamic input size from model metadata.
    """
    input_size = _get_arcface_input_size()
    resized = cv2.resize(face_img, (input_size, input_size))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    normalized = rgb.astype(np.float32) / 127.5 - 1.0
    transposed = normalized.transpose(2, 0, 1)[None]
    return transposed


def _preprocess_for_arcface_batch(face_imgs: list[np.ndarray]) -> np.ndarray:
    """
    OPTIMIZATION: Batch preprocess multiple faces for ArcFace.
    Significantly faster than processing one at a time.

    Args:
        face_imgs: List of face image crops (BGR format)

    Returns:
        Batched preprocessed tensor of shape (N, 3, input_size, input_size)
    """
    if len(face_imgs) == 0:
        return np.array([])

    input_size = _get_arcface_input_size()
    batch = []

    for face_img in face_imgs:
        resized = cv2.resize(face_img, (input_size, input_size))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        normalized = rgb.astype(np.float32) / 127.5 - 1.0
        transposed = normalized.transpose(2, 0, 1)
        batch.append(transposed)

    return np.array(batch)


# ========== SHARED FACE DETECTION ==========
def detect_single_face(image: np.ndarray) -> np.ndarray | None:
    """
    Detect single face in image (for enrollment).
    Returns cropped face or None if no face detected.

    Uses NMS to handle multiple detections and returns the highest confidence face.
    """
    h, w = image.shape[:2]
    preprocessed = _preprocess_for_yolo(image)

    yolo_session = _get_yolo_session()
    input_name = _get_yolo_input_name()

    # Run inference
    raw_outputs = yolo_session.run(None, {input_name: preprocessed})

    # Inspect model on first run
    global _yolo_output_format
    if _yolo_output_format is None:
        _inspect_yolo_model()

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
    keep_indices = _apply_nms(boxes, scores, iou_threshold=0.45)

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
    """
    h, w = image.shape[:2]
    preprocessed = _preprocess_for_yolo(image)

    yolo_session = _get_yolo_session()
    input_name = _get_yolo_input_name()

    # Run inference
    raw_outputs = yolo_session.run(None, {input_name: preprocessed})

    # Inspect model on first run
    global _yolo_output_format
    if _yolo_output_format is None:
        _inspect_yolo_model()

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
    keep_indices = _apply_nms(boxes, scores, iou_threshold=0.45)

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


# ========== SHARED EMBEDDING EXTRACTION ==========
def extract_embedding(face_img: np.ndarray) -> list[float]:
    """
    Extract 512-dimensional embedding from face image.
    Returns normalized embedding vector.

    Raises:
        ValueError: If face image is invalid or embedding extraction fails
    """
    # Validate input
    if face_img is None or face_img.size == 0:
        raise ValueError("Invalid face image: empty or None")

    preprocessed = _preprocess_for_arcface(face_img)

    arcface_session = _get_arcface_session()
    input_name = _get_arcface_input_name()
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
    OPTIMIZATION: Batch extract embeddings from multiple face images.
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
    preprocessed_batch = _preprocess_for_arcface_batch(face_imgs)

    # Run batch inference
    arcface_session = _get_arcface_session()
    input_name = _get_arcface_input_name()
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