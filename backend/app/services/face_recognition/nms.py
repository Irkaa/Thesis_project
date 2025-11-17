"""
Non-Maximum Suppression utilities.
Removes duplicate bounding box detections.
"""
import cv2
import numpy as np
from app.utils.config import FACE_DETECTION_THRESHOLD


def apply_nms(boxes, scores, iou_threshold=0.45):
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
