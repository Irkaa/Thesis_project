from fastapi import FastAPI
from app.routes import students

app = FastAPI(
    title="Student Attendance System API",
    description="Handles student data management and facial recognition operations.",
    version="1.0.0",
)

app.include_router(students.router)

@app.get("/")
async def root():
    return {"message": "Backend is running successfully"}
