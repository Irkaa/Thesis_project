from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import test_db

app = FastAPI(title="Student Attendance System API")

# Allow frontend (Next.js) to connect
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_db.router)

@app.get("/")
async def root():
    return {"message": "Backend connected successfully!"}
