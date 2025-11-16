# Face Attendance System - Skeleton

## Quick start (backend)
1. cd backend
2. python -m venv .venv
3. source .venv/bin/activate
4. pip install -r requirements.txt
5. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Quick start (backend) with docker
    1. cd root
    2. docker-compose up 
Check logs :
    3. docker logs face_backend -f
Rebuild image (only if requriements.txt or Dockerfile changed)
    4. docker-compose build --no-cache
Restart backend container:
    5. docker-compose restart backend

Reset database :
   6. docker-compose down -v
    docker-compose up

## Frontend
Open `frontend/index.html` in your browser for manual testing.

