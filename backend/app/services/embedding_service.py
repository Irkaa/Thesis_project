# This function is used by the endpoint to generate a 512-dim embedding.

import numpy as np
import cv2
from insightface.app import FaceAnalysis


# Load ArcFace model once
face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=0, det_size=(640, 640))


def extract_embedding_from_image(image_bytes: bytes):
    jpg = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)

    faces = face_app.get(img)

    if len(faces) == 0:
        return None

    face = faces[0]
    return face.normed_embedding.tolist()
