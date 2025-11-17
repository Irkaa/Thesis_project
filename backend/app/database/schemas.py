from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import datetime

class StudentBase(BaseModel):
    student_id: str
    name: str
    email: str
    class_name: str
    photo_url: Optional[str] = None

class ClassBase(BaseModel):
    class_name: str
    teacher_id: Optional[str] = None
    semester: Optional[str] = None
    department: Optional[str] = None


class ClassUpdate(BaseModel):
    class_name: Optional[str]
    teacher_id: Optional[str]
    semester: Optional[str]
    department: Optional[str]

class ClassSessionBase(BaseModel):
    class_id: str
    date: str
    start_time: str
    end_time: str
    location: Optional[str] = None
    session_type: Optional[str] = None


class ClassSessionUpdate(BaseModel):
    class_id: Optional[str]
    date: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    location: Optional[str]
    session_type: Optional[str]

class RecognitionLogBase(BaseModel):
    student_id: Optional[str] = None          # matched student_id, if any
    event_time: Optional[datetime] = None
    confidence: Optional[float] = None
    camera_id: Optional[str] = None
    status: Optional[str] = None              # e.g., "matched", "no_face", "multiple_faces"
    raw_face_capture_s3_url: Optional[str] = None
    embedding_vector: Optional[list[Any]] = None
    matched_student_id: Optional[str] = None
    distance_score: Optional[float] = None
    session_id: Optional[str] = None

class RecognitionLogCreate(RecognitionLogBase):
    # event_time can be omitted; created server-side if not provided
    pass

class RecognitionLogQuery(BaseModel):
    student_id: Optional[str] = None
    session_id: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

class StudentEmbeddingBase(BaseModel):
    student_id: str
    embedding: list[float]
    photo_s3_url: Optional[str] = None
    version: Optional[int] = 1
    created_at: Optional[datetime] = None

class AttendanceCreate(BaseModel):
    student_id: str
    session_id: str
    status: str = "present"
    recognized_confidence: Optional[float] = None


class AttendanceResponse(BaseModel):
    attendance_id: str
    student_id: str
    session_id: str
    recognized_time: datetime
    status: str
    recognized_confidence: Optional[float] = None

class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str   # raw plain password (only for input)
    role: str = "teacher" 

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str