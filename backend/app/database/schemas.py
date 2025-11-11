from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    student_id: str
    name: str
    email: str
    class_name: str
    photo_url: Optional[str] = None
