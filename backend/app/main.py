from fastapi import FastAPI
from app.routes import (
    students, attendance, classes, class_sessions, recognition_logs, student_embeddings, recognition, auth
)
app = FastAPI(
    title="Student Attendance System API",
    description="Handles student data management and facial recognition operations.",
    version="1.0.0",
)

# Register both routers
app.include_router(students.router)
app.include_router(attendance.router)
app.include_router(classes.router)
app.include_router(class_sessions.router)   
app.include_router(recognition_logs.router)
app.include_router(student_embeddings.router)
app.include_router(recognition.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Backend is running successfully"}
