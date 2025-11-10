from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class StudentModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="id")
    student_id: str
    name: str
    class_name: str
    photo_url: Optional[str] = None
    embedding: Optional[List[float]] = None  # for facial features

    class Config:
        populate_by_name = True  # updated for Pydantic v2
        json_encoders = {datetime: lambda v: v.isoformat()}


class AttendanceModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="id")
    student_id: str
    date: datetime
    status: str  # Present / Absent

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="id")
    username: str
    password: str
    role: Optional[str] = "teacher"
