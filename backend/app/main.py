from fastapi import FastAPI
from app.routes import students, attendance  # ← include attendance here

app = FastAPI(
    title="Student Attendance System API",
    description="Handles student data management and facial recognition operations.",
    version="1.0.0",
)

# Register both routers
app.include_router(students.router)
app.include_router(attendance.router)

@app.get("/")
async def root():
    return {"message": "Backend is running successfully"}
