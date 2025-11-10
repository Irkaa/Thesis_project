from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Used for request/response validation

class StudentCreate(BaseModel):
    student_id: str
    name: str
    class_name: str
    photo_url: Optional[str] = None

class AttendanceCreate(BaseModel):
    student_id: str
    date: datetime
    status: str

class UserCreate(BaseModel):
    username: str
    password: str
