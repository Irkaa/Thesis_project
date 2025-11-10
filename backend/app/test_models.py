from app.database.models import StudentModel, AttendanceModel, UserModel
from app.database.schemas import StudentCreate, AttendanceCreate, UserCreate
from datetime import datetime

def test_models():
    # Create mock student
    student = StudentModel(
        student_id="S001",
        name="John Doe",
        class_name="CS101",
        photo_url="https://example.com/photo.jpg",
        embedding=[0.1, 0.2, 0.3]
    )
    print("✅ Student model loaded:", student.model_dump())

    # Create mock attendance record
    attendance = AttendanceModel(
        student_id="S001",
        date=datetime.now(),
        status="Present"
    )
    print("✅ Attendance model loaded:", attendance.model_dump())

    # Create mock user
    user = UserModel(
        username="teacher1",
        password="securepass",
        role="teacher"
    )
    print("✅ User model loaded:", user.model_dump())

def test_schemas():
    # Create request schema samples
    student_req = StudentCreate(student_id="S002", name="Jane Smith", class_name="IT202")
    print("✅ StudentCreate schema valid:", student_req.model_dump())

    attendance_req = AttendanceCreate(student_id="S002", date=datetime.now(), status="Absent")
    print("✅ AttendanceCreate schema valid:", attendance_req.model_dump())

    user_req = UserCreate(username="teacher2", password="mypassword")
    print("✅ UserCreate schema valid:", user_req.model_dump())


if __name__ == "__main__":
    test_models()
    test_schemas()
