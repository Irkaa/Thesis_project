import numpy as np
from typing import List, Dict
from app.database.connection import db
from app.database.models import student_helper
from bson import ObjectId
import cv2
from insightface.app import FaceAnalysis


# ---------------------------
# LOAD MODELS (ONE TIME ONLY)
# ---------------------------
face_app = FaceAnalysis(
    name="buffalo_l",  # includes: SCRFD detector + ArcFace model
    providers=["CPUExecutionProvider"]
)
face_app.prepare(ctx_id=0, det_size=(640, 640))


# ---------------------------
# SETTINGS
# ---------------------------
SIMILARITY_THRESHOLD = 0.48     # ArcFace recommended: 0.4–0.5
FACE_SIZE_LIMIT = 40            # ignore tiny faces
MAX_STUDENTS_IN_CLASS = 200     # for faster matching


# ---------------------------
# DATABASE COLLECTIONS
# ---------------------------
students_collection = db["students"]
embeddings_collection = db["student_embeddings"]


# ---------------------------
# Helper: get all registered embeddings
# ---------------------------
async def load_all_embeddings():
    cursor = embeddings_collection.find({})
    student_ids = []
    embedding_vectors = []

    async for doc in cursor:
        student_ids.append(doc["student_id"])
        embedding_vectors.append(np.array(doc["embedding"], dtype=np.float32))

    return student_ids, np.array(embedding_vectors, dtype=np.float32)


# ---------------------------
# Helper: cosine similarity
# ---------------------------
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ---------------------------
# Helper: match ONE face embedding against all students
# ---------------------------
def match_face(embedding: np.ndarray, all_ids: List[str], all_embs: np.ndarray):
    if len(all_embs) == 0:
        return None, 0.0

    scores = np.dot(all_embs, embedding) / (
        np.linalg.norm(all_embs, axis=1) * np.linalg.norm(embedding)
    )

    best_idx = int(np.argmax(scores))
    best_score = float(scores[best_idx])

    if best_score < SIMILARITY_THRESHOLD:
        return None, best_score

    return all_ids[best_idx], best_score


# ---------------------------
# PROCESS A SINGLE IMAGE
# ---------------------------
def process_single_image(image_bytes: bytes, all_ids, all_embs):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    faces = face_app.get(img)
    results = []

    for face in faces:
        if face.bbox is None:
            continue

        # Filter tiny faces
        x1, y1, x2, y2 = map(int, face.bbox)
        if (x2 - x1) < FACE_SIZE_LIMIT or (y2 - y1) < FACE_SIZE_LIMIT:
            continue

        # Get embedding (512 vector)
        embedding = face.embedding

        # Match to student DB
        student_id, score = match_face(embedding, all_ids, all_embs)

        if student_id is not None:
            results.append({
                "student_id": student_id,
                "similarity": score
            })

    return results


# ---------------------------
# MAIN PIPELINE: MULTIPLE IMAGES
# ---------------------------
async def recognize_multiple_images_service(images: List[bytes]):
    # 1. Load all embeddings from DB
    all_ids, all_embs = await load_all_embeddings()

    # 2. Storage for matches
    detected_students = {}

    # 3. Process each image
    for img_bytes in images:
        matches = process_single_image(img_bytes, all_ids, all_embs)

        for m in matches:
            sid = m["student_id"]
            score = m["similarity"]

            # Keep highest similarity across all images
            if sid not in detected_students or score > detected_students[sid]:
                detected_students[sid] = score

    # Convert to final list
    present_list = [
        {"student_id": sid, "similarity": detected_students[sid]}
        for sid in detected_students
    ]

    return present_list
